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
    'x2' : '00110' ,
    'x6' : '00111' ,
    'x7' : '00000' ,
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
op = '0101111'
dict_opcode = {
    'lr.w' : op,
    'sc.w' : op,
    'amoadd.w' : op,
    'amoand.w' : op,
    'amomax.w' : op,
    'amomaxu.w'  : op,
    'amomin.w'  : op,
    'amominu.w' : op,
    'amoor.w' : op,
    'amoswap.w' : op,
    'amoxor.w' : op,
    }

# khai báo funct3
f3 = '010'
dict_funct3 = {
    'lr.w' : f3,
    'sc.w' : f3,
    'amoadd.w' : f3,
    'amoand.w' : f3,
    'amomax.w' : f3,
    'amomaxu.w'  : f3,
    'amomin.w'  : f3,
    'amominu.w' : f3,
    'amoor.w' : f3,
    'amoswap.w' : f3,
    'amoxor.w' : f3,
    }

# khai báo 2 bit aquire và release trong funct7
dict_mop ={
    '''
    truy cập bộ nhớ không đồng bộ. Điều này có nghĩa là không có
    yêu cầu cụ thể về sự đồng bộ hóa nào đối với truy cập này. 
    Thông thường, truy cập không đồng bộ sẽ không đảm bảo thứ tự của các 
    truy cập khác nhau và không có cơ chế bảo vệ dữ liệu chia sẻ.
    '''
    
    'asynchronous' : '00',
    
    '''
    truy cập bộ nhớ với release. Truy cập này được xác định là kết thúc một 
    loạt các truy cập đồng bộ hoặc sửa đổi bộ nhớ. Trong một loạt các truy cập, 
    truy cập cuối cùng
    được ghi nhận là release, cho phép các truy cập khác đồng bộ với nó.
    '''
    
    'release' : '01',
    
    '''
    Truy cập bộ nhớ với acquire. Truy cập này được xác định là bắt đầu 
    một loạt các truy cập đồng bộ. Trong một loạt các truy cập, truy cập 
    đầu tiên được ghi nhận là acquire,
    cho phép các truy cập khác đồng bộ với nó.
    '''
   
    'accquire' : '10',
   
    '''
    Truy cập bộ nhớ đồng bộ hoàn toàn. Truy cập này được xác định là cả bắt 
    đầu và kết thúc một loạt các truy cập đồng bộ. Trong một loạt các 
    truy cập, truy cập đầu tiên được ghi nhận là acquire và truy cập cuối cùng 
    được ghi nhận là release, phép các truy cập khác đồng bộ với nó.
    '''
   
    'synchronous' : '11'
    }

dict_funct5 = {
    'lr.w' : '00010',
    'sc.w' : '00011',
    'amoadd.w' : '00000',
    'amoand.w' : '01100',
    'amomax.w' : '10100',
    'amomaxu.w'  : '11100',
    'amomin.w'  : '10000',
    'amominu.w' : '11000',
    'amoor.w' : '01000',
    'amoswap.w' : '00001',
    'amoxor.w' : '00100',
    }

dict_ins = {
    '32A' : ['lr.w', 'sc.w' , 'amoswap.w', 'amoadd.w', 'amoxor.w', 'amoand.w', 'amomax.w'
             ,'amomaxu.w', 'amomin.w', 'amominu.w', 'amoor.w' ]
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
def Atomic(a,label):
    global dict_funct5, dict_mop, dict_reg, dict_funct3, dict_opcode
    if a[0] in dict_ins['32A']:
        if a[1] not in dict_reg.keys() and a[2] not in dict_reg.keys():
            raise Exception("The register in rd and rs1 field must be Integer Register x0-x31")
    else:
        if a[1] not in dict_reg.keys() and a[2] not in dict_reg.keys() and a[3] not in dict_reg.keys():   
            raise Exception("The register in rd and rs2 and rs1 field must be Integer Register x0-x31")
    
    #lệnh lr.w không sử dụng RS2 nên mặc định là bằng 00000
    if a[0] == 'lr.w': # còn thiếu 2 bit aq và rl
        return dict_funct5[a[0]] + '00' + '00000' + dict_reg[a[2]] + dict_funct3[a[0]] + dict_reg[a[1]] + dict_opcode[a[0]]
    else: # còn thiếu 2 bit aq và rl
        return dict_funct5[a[0]] + '11' + dict_reg[a[2]] + dict_reg[a[3]] + dict_funct3[a[0]] + dict_reg[a[1]] + dict_opcode[a[0]]

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

'''
Hàm recursive nhận vào đường dẫn a và thư mục đầu ra out. Nó đệ quy qua tất cả các tệp và thư mục trong thư mục a để tìm và xử lý các tệp văn bản .S.

Nếu a là một thư mục, nó thay đổi thư mục làm việc đến a và gọi lại chính nó để xử lý các tệp và thư mục con trong a.

Nếu a là một tệp văn bản và kết thúc bằng .S, nó đọc nội dung của tệp, xử lý nội dung để tạo ra các lệnh assembly, sau đó ghi các lệnh này vào một tệp văn bản mới có tên là {tên tệp gốc}.txt trong thư mục đầu ra.

Nếu a không phải là một thư mục và không kết thúc bằng .S, nó tiếp tục duyệt qua các phần tử khác.
'''
'''
def process_w_file(file_path, out):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines, label = FileSetup(lines)
    ins = []
    for line in lines:
        if line[0] in dict_ins['32A']:
            ins.append(Atomic(line, label))
        else:
            raise Exception("Invalid Instruction")
    ins = '\n'.join(ins)
    ins += '\n'
    file_name = "output.txt"
    with open(os.path.join(out, file_name), 'w') as f:
        f.write(ins)

def ScanFile(out):
    file_path = r"E:\SaveFilePython\Assembler\Test1\Ass1.txt"
    if os.path.isfile(file_path):
        process_w_file(file_path, out)
        
output_dir = r"E:\SaveFilePython\Assembler\Out"
ScanFile(output_dir)
'''
def process_w_file(file_path, out):
    ins = []
    d = file_path.replace(os.getcwd().replace('\\', '/') + '/', '')
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines, label = FileSetup(lines)
    for line in lines:
        if line[0] in dict_opcode.keys():
            ins.append(Atomic(line, label))
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















    
'''
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
'''


