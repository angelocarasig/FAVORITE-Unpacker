#!/usr/bin/python3
import os, sys, struct
import marshal
from io import BytesIO

SD_FUNCTIONS = 0
SD_MAIN_SCRIPT = 3
SD_EXTRA_BINARY_DATA = 4
FN_POS = 0
FN_ID = 1
FN_ARGS = 2

opcodes = {
    0x00: [],
    0x01: ['b', 'b'],   #unknown
    0x02: ['d'],        #call function
    0x03: ['w'],        #unknown
    0x04: [],           #retn?
    0x05: [],           #retn?
    0x06: ['d'],        #jump?
    0x07: ['d'],        #cond jump?
    0x08: [],           #unknown
    0x09: [],           #unknown
    0x0a: ['d'],        #unknown
    0x0b: ['w'],        #unknown
    0x0c: ['b'],        #unknown
    0x0d: [],           #empty
    0x0e: ['s'],        #string
    0x0f: ['w'],        #unknown
    0x10: ['b'],        #unknown
    0x11: ['w'],        #unknown
    0x12: ['b'],        #unknown
    0x13: [],
    0x14: [],           #unknown
    0x15: ['w'],        #unknown
    0x16: ['b'],        #unknown
    0x17: ['w'],        #unknown
    0x18: ['b'],        #unknown
    0x19: [],           #unknown
    0x1a: [],           #unknown
    0x1b: [],           #unknown
    0x1c: [],           #unknown
    0x1d: [],           #unknown
    0x1e: [],           #unknown
    0x1f: [],           #unknown
    0x20: [],           #unknown
    0x21: [],           #unknown
    0x22: [],           #unknown
    0x23: [],           #unknown
    0x24: [],           #unknown
    0x25: [],           #unknown
    0x26: [],           #unknown
    0x27: [],           #unknown
    0x33: [],
    0x3f: [],
    0x40: [],
    0xb3: [],
    0xb8: [],
    0xd8: [],
    0xf0: [],
    0x52: [],
    0x9e: [],
}

def get_data(file_name):
    with open(file_name, 'rb') as file:
        return file.read()

def get_func_size(func):
    opcode_id = func[FN_ID]
    size = 1
    for i, type in enumerate(opcodes[opcode_id]):
        arg = func[FN_ARGS][i]
        if type == 'b':
            size += 1
        elif type == 'w':
            size += 2
        elif type == 'd':
            size += 4
        elif type == 's':
            size += 1
            size += len(arg[1])
            size += 1
        else:
            raise AssertionError('Bad argument')
    return size

def read_func(io, strings):
    pos = io.tell()
    opcode_id = struct.unpack('B', io.read(1))[0]
    if opcode_id not in opcodes:
        raise RuntimeError('Unknown opcode: %x at loc: %x' % (opcode_id, pos))

    func = {
        FN_POS: pos,
        FN_ID: opcode_id,
        FN_ARGS: []
    }

    for type in opcodes[opcode_id]:
        if type == 'b':
            func[FN_ARGS].append(struct.unpack('B', io.read(1))[0])
        elif type == 'w':
            func[FN_ARGS].append(struct.unpack('<H', io.read(2))[0])
        elif type == 'd':
            func[FN_ARGS].append(struct.unpack('<I', io.read(4))[0])
        elif type == 's':
            string_len = struct.unpack('B', io.read(1))[0]
            string = io.read(string_len)[:-1]
            func[FN_ARGS].append([len(strings), string])
            strings.append(string)
        else:
            raise AssertionError('Bad argument')

    return func

def write_func(io, func):
    opcode_id = func[FN_ID]
    if opcode_id not in opcodes:
        raise RuntimeError('Unknown script opcode: %s' % opcode_id)

    io.write(struct.pack('B', opcode_id))

    for i, type in enumerate(opcodes[opcode_id]):
        arg = func[FN_ARGS][i]
        if type == 'b':
            io.write(struct.pack('B', arg))
        elif type == 'w':
            io.write(struct.pack('<H', arg))
        elif type == 'd':
            io.write(struct.pack('<I', arg))
        elif type == 's':
            try:
                io.write(struct.pack('B', len(arg[1]) + 1))
            except:
                print(f"Length of line is too long...\nLine: {arg}\nLine Length: {len(arg[1]) + 1}\n")
                raise RuntimeError()

            io.write(arg[1])
            io.write(b'\0')
        else:
            raise AssertionError('Bad argument')

def decompile(file_name):
    file_data = BytesIO(get_data(file_name))
    script_len = struct.unpack('<I', file_data.read(4))[0]
    file_data.seek(script_len)
    main_script_start = struct.unpack('<I', file_data.read(4))[0]

    script_data = {
        SD_FUNCTIONS: [],
        SD_MAIN_SCRIPT: [],
        SD_EXTRA_BINARY_DATA: None,
    }
    strings = []

    file_data.seek(4)
    target = script_data[SD_FUNCTIONS]
    while file_data.tell() < script_len:
        if file_data.tell() == main_script_start:
            target = script_data[SD_MAIN_SCRIPT]

        func = read_func(file_data, strings)
        target.append(func)

    file_data.seek(script_len + 4)
    script_data[SD_EXTRA_BINARY_DATA] = file_data.read()

    with open('script.dat', 'wb') as script_file:
        marshal.dump(script_data, script_file)
    with open('strings.txt', 'wb') as strings_file:
        strings_file.write(b"\n".join(strings).decode('sjis').encode('utf-8'))

def compile(file_name):
    script_data = marshal.loads(get_data('script.dat'))
    strings = get_data('strings.txt').decode('utf-8')
    strings = strings.encode('sjis')
    strings = strings.splitlines()

    #prepare jump translation table
    pos = 4
    jump_table = {}
    for section in [SD_FUNCTIONS, SD_MAIN_SCRIPT]:
        if section == SD_MAIN_SCRIPT:
            main_script_start = pos
        for func in script_data[section]:
            if func[FN_ID] == 0xe:
                func[FN_ARGS][0][1] = strings[func[FN_ARGS][0][0]]
            jump_table[func[FN_POS]] = pos
            pos += get_func_size(func)

    #construct real data
    new_file_data = BytesIO()
    for section in [SD_FUNCTIONS, SD_MAIN_SCRIPT]:
        for i, func in enumerate(script_data[section]):
            if func[FN_ID] in [2, 6, 7]:
                func[FN_ARGS][0] = jump_table[func[FN_ARGS][0]]
            elif func[FN_ID] == 0xa:
                prev_func = script_data[section][i - 1]
                try:
                    #0xa preceded by 2 most likely means a sound file number;
                    #sound file numbers shouldn't be translated.
                    #(other than that, I really have no idea what I'm doing.)
                    if prev_func[FN_ID] != 2:
                        func[FN_ARGS][0] = jump_table[func[FN_ARGS][0]]
                except:
                    pass
            write_func(new_file_data, func)

    with open(file_name, 'wb') as hcb_file:
        hcb_file.write(struct.pack('<I', new_file_data.tell() + 4))
        hcb_file.write(new_file_data.getvalue())
        hcb_file.write(struct.pack('<I', main_script_start))
        hcb_file.write(script_data[SD_EXTRA_BINARY_DATA])

def main():
    if len(sys.argv) == 3:
        if sys.argv[1] == '-d':
            decompile(sys.argv[2])
            return
        elif sys.argv[1] == '-c':
            compile(sys.argv[2])
            return
    print('Usage: script.py -d input.hcb')
    print('Usage: script.py -c output.hcb')
    print('-d: extracts strings.txt + script.dat from the input.hcb script file')
    print('-c: compiles strings.txt + script.dat back into an output.hcb script file to use in game')

if __name__ == '__main__':
    main()
