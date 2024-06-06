.DATA
.TEXT
MAIN:
lr.w x20, x0 # x20 = 10		//4
sc.w x30, x12, x0		//8
amoxor.w x20, x14, x0		/12
amoadd.w x21, x15, x14 		//16
amoand.w x20, x12, x0		//20
amoor.w x21, x13, x13		//24
amomax.w x20, x11, x0		//28
amomaxu.w x21, x12, x14		//32
amoswap.w x11, x11 , x0 	//36
amomin.w x20, x11, x0		//40
amomin.w x21, x12, x14		//44
//HEHEHE
#COMMENT
