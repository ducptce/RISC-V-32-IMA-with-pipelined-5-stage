import os
import argparse

#Chuyen bin sang hex
dict_hex = {
    '0000' : '0',
    '0001' : '1',
    '0010' : '2',
    '0011' : '3',
    '0100' : '4',
    '0101' : '5',
    '0110' : '6',
    '0111' : '7',
    '1000' : '8',
    '1001' : '9',
    '1010' : 'A',
    '1011' : 'B',
    '1100' : 'C',
    '1101' : 'D',
    '1110' : 'E',
    '1111' : 'F'
    }
#khai báo các thanh ghi
Reg = {
       'zero'   : 'x0',
       'ra'     : 'x1',
       'sp'     : 'x2',
       'gp'     : 'x3',
       'tp'     : 'x4',
       't0'     : 'x5',
       't1'     : 'x6',
       't2'     : 'x7',
       's0'     : 'x8',
       'fp'     : 'x8',
       's1'     : 'x9',
       'a0'     : 'x10',
       'a1'     : 'x11',
       'a2'     : 'x12',
       'a3'     : 'x13',
       'a4'     : 'x14',
       'a5'     : 'x15',
       'a6'     : 'x16',
       'a7'     : 'x17',
       's2'     : 'x18',
       's3'     : 'x19',
       's4'     : 'x20',
       's5'     : 'x21',
       's6'     : 'x22',
       's7'     : 'x23',
       's8'     : 'x24',
       's9'     : 'x25',
       's10'    : 'x26',
       's11'    : 'x27',
       't3'     : 'x28',
       't4'     : 'x29', 
       't5'     : 'x30', 
       't6'     : 'x31',
       }
dict_reg = {
    'x0' : '00000' ,
    'x1' : '00001' ,
    'x2' : '00010' ,
    'x3' : '00011' ,
    'x4' : '00100' ,
    'x5' : '00101' ,
    'x6' : '00110' ,
    'x7' : '00111' ,
    'x8' : '01000' ,
    'x9' : '01001' ,
    'x10' : '01010' ,
    'x11' : '01011' ,
    'x12' : '01100' ,
    'x13' : '01101' ,
    'x14' : '01110' ,
    'x15' : '01111' ,
    'x16' : '10000' ,
    'x17' : '10001' ,
    'x18' : '10010' ,
    'x19' : '10011' ,
    'x20' : '10100' ,
    'x21' : '10101' ,
    'x22' : '10110' ,
    'x23' : '10111' ,
    'x24' : '11000' ,
    'x25' : '11001' ,
    'x26' : '11010' ,
    'x27' : '11011' ,
    'x28' : '11100' ,
    'x29' : '11101' ,
    'x30' : '11110' ,
    'x31' : '11111' 
    }

#khai báo opcode
op = '0110011'
dict_opcode = {
    'mul' : op,
    'mulh' : op,
    'mulhsu' : op,
    'mulhu' : op,
    'div' : op,
    'divu'  : op,
    'rem'  : op,
    'remu': op,
    }

# khai báo funct3
dict_funct3 = {
    'mul' : '000',
    'mulh' : '001',
    'mulhsu' : '010',
    'mulhu' : '011',
    'div' : '100',
    'divu'  : '101',
    'rem'  : '110',
    'remu': '111',
    }

f7 = '0000001'
dict_funct7 = {
    'mul' : f7,
    'mulh' : f7,
    'mulhsu' : f7,
    'mulhu' : f7,
    'div' : f7,
    'divu'  : f7,
    'rem'  : f7,
    'remu': f7,
    }

# dùng để chuyển đổi giá trị Imme
def decimal_to_binary(decimal_num):
    binary_num = ""
    
    # Chia liên tục cho 2 và lưu dư vào chuỗi nhị phân
    while decimal_num > 0:
        remainder = decimal_num % 2
        binary_num = str(remainder) + binary_num
        decimal_num //= 2
    
    # Thêm các số 0 vào đầu chuỗi để đảm bảo có 5 bit
    while len(binary_num) < 5:
        binary_num = '0' + binary_num
    
    return binary_num[-5:]


#form instr Rd, Rs2, Rs1
def Multiplication_and_Division(a,label):
    global dict_funct7, dict_reg, dict_funct3, dict_opcode
    if a[0] in dict_opcode.keys():
        if a[1] not in dict_reg.keys() and a[2] not in dict_reg.keys():
            raise Exception("The register in rd and rs1 field must be Integer Register x0-x31")
    else:
        if a[1] not in dict_reg.keys() and a[2] not in dict_reg.keys() and a[3] not in dict_reg.keys():   
            raise Exception("The register in rd and rs2 and rs1 field must be Integer Register x0-x31")
    
    if a[0] in dict_opcode.keys():
        return dict_funct7[a[0]] + dict_reg[a[3]] + dict_reg[a[2]] + dict_funct3[a[0]] + dict_reg[a[1]] + dict_opcode[a[0]]
   
def FileSetup(a):
    label =[]
    ins = []
    idx = 0
    for i in range(len(a)):
        if a[i].find('#') != -1:
            #Nếu phần tử thứ i chứa ký tự "#", thì loại bỏ từ ký tự "#" trở đi trong phần tử đó.
            a[i] = a[i].replace(a[i][a[i].find('#'):], '') 
        if a[i].find('/') != -1:
            a[i] = a[i].replace(a[i][a[i].find('/'):], '')
            #Nếu phần tử thứ i chứa ký tự "(", thì thay thế ký tự "(" bằng khoảng trắng trong phần tử đó.
        if a[i].find('(') != -1:
            a[i] = a[i].replace('(', ' ')
        if a[i].find(')') != -1:
            a[i] = a[i].replace(')', ' ')
        if a[i].find(',') != -1:
            a[i] = a[i].replace(',', ' ')
        a[i] = a[i].split()
        print(a[i])
    a = [i for i in a if i != [] and i[0].lower() not in ['.data', '.text']]  
    print(a)
    for i in a:
        if len(i) > 1:
            # endswith()	Returns true if the string ends with the specified value
            if i[0].endswith(":"): 
                label.append([i[0], idx])
                idx = idx + 4
                i.remove(i[0])
            else:
                idx = idx + 4
        else:
            if i[0].endswith(":"): 
                label.append([i[0], idx])
                a.remove(i)
    a = [i + [j*4] for j , i in enumerate(a)]
    return a, label

def process_w_file(file_path, out):
    ins = []
    d = file_path.replace(os.getcwd().replace('\\', '/') + '/', '')
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line in lines == range(32):
            # Gọi DecoderIme để nhận các giá trị trả về
            funct7, funct3, imm, rs2, rs1, rd, opcode, shamt = DecoderIme(line)
            # Truyền các giá trị đã nhận được vào hàm Simulator
            ins.append(Simulator(funct7, funct3, imm, rs2, rs1, rd, opcode, shamt))
        else:
            raise Exception("Invalid Instruction")
    ins = '\n'.join(ins)
    ins += '\n'
    file_name = os.path.basename(file_path).split('.')[0] + '.txt'
    with open(os.path.join(out, file_name), 'w') as f:
        f.write(ins)

def ScanFile(a, out):
    try:
        os.chdir(a)
    except NotADirectoryError:
        if a.endswith('.txt'):
            process_w_file(a, out)
        return
    for entry in os.listdir():
        if os.path.isfile(os.path.join(a, entry)) and entry.endswith('.txt'):
            process_w_file(os.path.join(a, entry), out)
        elif os.path.isdir(os.path.join(a, entry)):
            ScanFile(os.path.join(a, entry), out)
    os.chdir(os.path.dirname(os.getcwd()))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", help="-o: Directory where the binary files are generated in")
    ap.add_argument("-i", "--input", help="-i: Directory of assembly files that should be converted to binary files recursively")
    args = ap.parse_args()

    if not args.output or not args.input:
        ap.error("Both input and output directories are required.")
    
    output_dir = args.output
    input_dir = args.input
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(input_dir):
        ap.error("Input directory does not exist.")

    os.chdir(output_dir)
    ScanFile(input_dir, output_dir)
