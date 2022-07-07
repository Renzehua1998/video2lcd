#include <REGX52.H>
#include "SD.h"
unsigned long  SD_ADDR=0;
unsigned int count;
unsigned char xdata DATA[512];
sbit E = P2^0;
sbit RW = P2^1;
sbit RS = P2^2;
sbit CS2 = P2^3;
sbit CS1 = P2^4;	//�˿ڶ���
#define DataPort P0
 /*12864��æ */
bit Chek_Busy(void)
{
    DataPort = 0xff;
    RW = 1;
    RS = 0;
    E = 1;
    E = 0;
    return (bit)(DataPort & 0x80);
}
/*------------------------------------------------
            ѡ��
i:0������,1������,2ȫ��
------------------------------------------------*/
void Choose_12864(unsigned char i)
{						 
   switch (i)			 
   {
       case 0: CS1 = 0;CS2 = 1;break;   
       case 1: CS1 = 1;CS2 = 0;break;
       case 2: CS1 = 0;CS2 = 0;break;
	   default: break;
   }
}
/*------------------------------------------------
        д����
------------------------------------------------*/
void LCD_Cmd(unsigned char cmd)
{
    while(Chek_Busy());
    RW = 0;	         
    RS = 0;
    DataPort = cmd;
    E = 1;
    E = 0;          
}
/*------------------------------------------------
        ��LCD
------------------------------------------------*/
unsigned char LCD_Read()
{
    unsigned char read_data;
    while(Chek_Busy());
    RW = 1;//�����һ�οն�
    RS = 1;
    E = 1;
    E = 0;

    RW = 1;
    RS = 1;
    E = 1;
    read_data = DataPort;
    E = 0;        
    return (read_data);    
}
/*------------------------------------------------
        д����
------------------------------------------------*/
void  LCD_Data(unsigned char dat)
{
    while(Chek_Busy());
    RW = 0;	         
    RS = 1;
    DataPort = dat;
    E = 1;
    E = 0; 
}
/*------------------------------------------------
             ���õ�ַ
PAGE:0-7;
Y_Address:0-63
------------------------------------------------*/
void Set_PageY(unsigned char PAGE,unsigned char Y_Address)
{
    LCD_Cmd(0xB8 + PAGE);
    LCD_Cmd(0x40 + Y_Address);
}
/*------------------------------------------------
                ����
------------------------------------------------*/
void LCD_Clear(void)
{
    unsigned char page,row;
    Choose_12864(2);
    for (page = 0xb8; page < 0xc0; page ++)
    {
        LCD_Cmd(page);
    	LCD_Cmd(0x40);
    	for (row = 0; row < 64; row ++)
    	{
    	    LCD_Data(0x00);//��12864���е�ַȫ��д��
    	}
    }
}
/*------------------------------------------------
               ��ʼ��
------------------------------------------------*/
void LCD_Init(void)
{
    CS2 = 0;
    CS1 = 0;
    LCD_Cmd(0x3F);//����ʾ
}
/*-------------------------------------------------
    ��ʾһ��12864ͼƬ
-------------------------------------------------*/
void Dis_Picture(unsigned char *picture)
{
    unsigned char ii,kk;
    for (kk = 0; kk < 4; kk ++)//LCD����7=8ҳ
    {
        Choose_12864(2);
        Set_PageY(kk,0);
        Choose_12864(0);        
        for (ii = 0; ii < 128; ii ++)
        {
            LCD_Data(*picture);
            picture ++;
            if (ii == 63)
            {
                Choose_12864(1);
            }
        }
    }
}
void Dis_Pictureb(unsigned char *picture)
{
    unsigned char ii,kk;
    for (kk = 4; kk < 8; kk ++)//LCD����7=8ҳ
    {
        Choose_12864(2);
        Set_PageY(kk,0);
        Choose_12864(0);        
        for (ii = 0; ii < 128; ii ++)
        {
            LCD_Data(*picture);
            picture ++;
            if (ii == 63)
            {
                Choose_12864(1);
            }
        }
    }
}
void delayus(unsigned char t)
{
    while(--t);
}
void delayms(unsigned char t)
{
    while(t--)
    {
        delayus(245);
        delayus(245);
    }
}
void main(void)
{
    char bb;
    bb=0;
    LCD_Init();
    LCD_Clear();
    SdInit();
    DATA[0]=255;;
    DATA[1]=1;
    DATA[2]=2;
    DATA[3]=3;
    DATA[511]=0xf0;
    //SdWriteBlock(DATA,2,512);
    while(1)
    {
        for(count=0;count<1093;count++)
        {
            while(!SdReadBlock(DATA,SD_ADDR,512));
            SD_ADDR+=512;
            Dis_Picture(DATA);
            while(!SdReadBlock(DATA,SD_ADDR,512));
            Dis_Pictureb(DATA);
            SD_ADDR+=512;
            delayms(50);
            bb++;
          }
     SD_ADDR=0;
    }
}