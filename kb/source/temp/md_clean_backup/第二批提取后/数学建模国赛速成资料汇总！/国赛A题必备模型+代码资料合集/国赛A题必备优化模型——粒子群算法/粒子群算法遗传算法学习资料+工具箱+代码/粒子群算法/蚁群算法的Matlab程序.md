#include<iostream.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

#define citynumber 5
#define Q 100
#define p 0.5
#define NM2 1000
#define A 1
#define B 5

int ccdi=-1;//全局变量,用在myrand()中
float myrand()//产生0-1随机数,100个,每调用一次,结果不同
{srand(time(0));
f潬瑡洠孹〱崰഻捣楤⬫഻晩⠠捣楤㴽〱⤰ഠ捣楤〽഻潦⡲湩⁴業〽活㱩〱㬰業⬫ഩ晻潬瑡映癡爽湡⡤┩〱〰㬰洍孹業㵝慦⽶〱〰㬰ൽ敲畴湲洠孹捣楤㭝納഍潤扵敬映歰橩搨畯汢⁥孔楣祴畮扭牥孝楣祴畮扭牥ⱝ潤扵敬渠捛瑩湹浵敢嵲捛瑩湹浵敢嵲椬瑮琠扡孵楣祴畮扭牥孝楣祴畮扭牥ⱝ湩⁴Ⱬ湩⁴ⱳ湩⁴Ⱪ湩⁴⁪ഩ⼯定义函数用于计算Pij
{
 //double A=0.5,B=0.5;
 double sumup,pkij,sumdown;
 sumdown=0;
for(int aTi=0;aTi<citynumber;aTi++)
 {
	 for(int aTj=0;aTj<citynumber;aTj++)
     aT[aTi][aTj]=pow(T[aTi][aTj],A);
 }
 for(int bni=0;bni<citynumber;bni++)
 {
	 for(int bnj=0;bnj<citynumber;bnj++)
     bn[bni][bnj]=pow(n[bni][bnj],B);
 }

 for (int can=0;can<citynumber;can++)//判断,除掉已经走过的城市
	{
		if(can==tabu[k][ci])
	{
		aT[i][can]=0;bn[i][can]=0;
	}
	}

 sumup=aT[i][j]*bn[i][j];
 for(int tj=0;tj<citynumber;tj++)
  sumdown=aT[i][tj]*bn[i][tj]+sumdown;
pkij=sumup/sumdown;
return pkij;
}

void main()
{	double city[citynumber][2]={{0,1},{0,2},{2,2},{2,4},{1,3}/*,{3,4},{4,7},{2,8},{3,9},{1,10},
{1,0},{2,1},{3,0},{4,9},{5,2},{6,2},{7,1},{8,6},{9,0},{10,3}*/}; /*城市坐标*/
    double d[citynumber][citynumber];   //L[j][k]是城市j to k距离
	  for(int j=0;j<citynumber;j++)

	  {d[j][k]=sqrt((city[j][0]-city[k][0])*(city[j][0]-city[k][0])+(city[j][1]-city[k][1])*(city[j][1]-city[k][1]));
//	 cout<<d[j][k]<<" ";
	  }//cout<<"\n";
	  }	                   /*计算距离,从j城市到k城市*/

/*	for (int cj=0;cj<10;cj++)
	     {float c=myrand();
	     cout<<c<<" "<<"\n";}*///输出随机数

   double n[citynumber][citynumber];
	for(int ni=0;ni<citynumber;ni++)
	{
		for(int j=0;j<citynumber;j++)
				}//cout<<"\n";
	} /*初始化visibility nij*/

	double L[citynumber];
	int shortest[citynumber];

	double T[citynumber][citynumber];
	for(int ti=0;ti<citynumber;ti++)
	{
		for (int j=0;j<citynumber;j++)
		{
	    		//cout<<T[ti][j]<<" ";
		}//cout<<"\n";
	}/*初始化t*/
	double changT[citynumber][citynumber];
//step2:

	for(int NC=0;NC<NM2;NC++)
{	for(int cti=0;cti<citynumber;cti++)
	{
		for (int j=0;j<citynumber;j++)
		{
	    changT[cti][j]=0;//cout<<changT[cti][j]<<" ";
		}//cout<<"\n";
	}	/*初始化changT*/

؀ौড়଒ఘ๸໠ᅐበᏤᐸᒨᓰᗮᘠោៜᦞᧀᧄ☀⚂⡮⢄⣲⤄⮘⮬ⱊⱸⱺⲌⶶⷌⷎ⸜㍚㍪㍬㎀㖈㖊ﳷﳷﳷﳷﳷﳷﳷﳷﳷﳷñᘆ蝨贱唃Ĉᘉ걨ݛ漀Ĩᘆ걨ݛ⤀؀ࠪࡐࡲ࢔࢖ࣀࣜࣸचलॊौঊড়৾਎ਖਦਮੈ੡ੴઅઇઈ଒ఘజొú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切úЀ摧宬	ᴀ؀㖊ýЄĀāొಂಚೢ೨ഴ඀ආැූย๮๴๸໠໦༖༜བཛྷརཤཨྜ࿠ီၖၰၴၶú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切úЀ摧宬	ᴀၶၸၺၼ႔ᅐᇤበኢኪ᎐ᏀᏤᐸᐼᑶᒨᓰᓴᔾᖂᖈᗈᗮᘠᘤᙒᚈᚊᚌú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切úЀ摧宬	ᴀᚌᛒ᜖᜜᝞ᝦអោៜᠬᠾᡀᡂᡸᣆᣌᤎᤖ᥼ᦞᧀᧄ⚂⚆⛊⛮⛴❒➆⟎ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切ú切úЀ摧宬	ᴀ	int tabu[citynumber][citynumber];//tabu[k][s]表示第k只蚂蚁,第s次循环所在的城市

		for (int i=0;i<citynumber;i++)
		tabu[tai][i]=0;
	}
	for (int tabui1=0;tabui1<citynumber;tabui1++)
		tabu[tabui1][0]=tabui1;
	/*for (tai=0;tai<citynumber;tai++)
	{
		for (int i=0;i<citynumber;i++)
		cout<<tabu[tai][i]<<" ";cout<<"\n";
	}*/
	//初始化tabu

	for(int kk=0;kk<citynumber;kk++)
    L[kk]=0;

	//第三步开始
for(int s=0;s<citynumber-1;s++)
{
	for(int k=0;k<citynumber;)
	{
    int ci,can;
	float sumpk=0;
	float pkij;

hq2: can++;
	 if (can==citynumber) can=0;
	 for (ci=0;ci<=s;ci++)
	 {if(can==tabu[k][ci]) goto hq2;}
	 pkij=fpkij(T,n,tabu,k,s,tabu[k][s],can);
	 sumpk=sumpk+pkij;
	     else goto hq2;
	 tabu[k][s+1]=can;
     k++;
	}
}	//第三步完成

 /*for (tai=0;tai<citynumber;tai++)
	{
		for (int i=0;i<citynumber;i++)

	}*///输出一个循环后的tabu[][]

//第四步开始

for(int k4=0;k4<citynumber;k4++)
   {
	s44=s4+1;
    if (s44==citynumber) s44=0;
    L[k4]+=d[tabu[k4][s4]][tabu[k4][s44]];
  }//cout<<L[k4]<<" ";
 }//计算L[k]

float shortest1=0; int short2=0;//最短距离
for(ii=1;shorti<citber;shi++ )
{
	shortest1=L[0];
    if(L[shorti]<=shortest1)
	{shortest1=L[shorti];short2=shorti;}
}
//cout<<L[sort2]<<"\n";cout<<short2<<"\n";
for(int shoi=0;shoi<ctynumber;shoi++)
{
shortest[shoi]=tabu[short2][shoi];
//cout<<shest[shoi]<<" ";
}
//cout<<"\n";

 for(int k41=0;k41<citynumber;k41++)
 {for(int s41=0,ss=0;s41<citynumber;s41++)
 {
	 ss=s41+1;
	 if (ss==citynumber) ss=0;
	 changT[tabu[k41][s41]][tabu[k41][ss]]+=Q/L[k41];
	 changT[tabu[k41][ss]][tabu[k41][s41]]=changT[tabu[k41][s41]][tabu[k41][ss]];
 }
 }
  /* for(int cti4=0;cti4<citynumber;cti4++)
	{
		for (int j=0;j<citynumber;j++)
		{cout<<changT[cti4][j]<<" ";}cout<<"\n";
	 }*/
 //第四步完

 // 第五步开始
  for(int i5=0;i5<citynumber;i5++)
  {
	 for(int j5=0;j5<citynumber;j5++)
	 {
		        // cout<<T[i5][j5]<<" ";
	 }
	//cout<<"\n";
  }

}

	 for(int shoi1=0;shoi1<citynumber;shoi1++)
{
cout<<city[shortest[shoi1]][0]<<" "<<city[shortest[shoi1]][1]<<"   ";
}

}
