#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define K 3 //������k
typedef float type;

//��ά����,��̬
type **createarray(int n,int m)
{
    int i;
    type **array;
    array=(type **)malloc(n*sizeof(type *));
    array[0]=(type *)malloc(n*m*sizeof(type));
    for(i=1;i<n;i++) array[i]=array[i-1]+m;
    return array;
}
//��ȡ���ݣ���ʽ N=������,D=ά��
void loaddata(int *n,int *d,type ***array,type ***karray)
{
    int i,j;
    FILE *fp;
    if((fp=fopen("data.txt","r"))==NULL)    fprintf(stderr,"can not open data.txt!\n");
    if(fscanf(fp,"N=%d,D=%d",n,d)!=2)    fprintf(stderr,"reading error!\n");
    *array=createarray(*n,*d);
    *karray=createarray(2,K);

    for(i=0;i<*n;i++)
        for(j=0;j<*d;j++)
            fscanf(fp,"%f",&(*array)[i][j]);    //��ȡ����

    for(i=0;i<2;i++)
        for(j=0;j<K;j++)
            (*karray)[i][j]=9999.0;    //Ĭ�ϵ����ֵ
    if(fclose(fp))    fprintf(stderr,"can not close data.txt");
}
//����ŷ�Ͼ���
type computedistance(int n,type *avector,type *bvector)
{
    int i;
    type dist=0.0;
    for(i=0;i<n;i++)
        dist+=pow(avector[i]-bvector[i],2);
    return sqrt(dist);
}
//ð������
void bublesort(int n,type **a,int choice)
{
    int i,j;
    type k;
    for(j=0;j<n;j++)
        for(i=0;i<n-j-1;i++){
            if(0==choice){
                if(a[0][i]>a[0][i+1]){
                    k=a[0][i];
                    a[0][i]=a[0][i+1];
                    a[0][i+1]=k;
                    k=a[1][i];
                    a[1][i]=a[1][i+1];
                    a[1][i+1]=k;
                }
            }
            else if(1==choice){
                if(a[1][i]>a[1][i+1]){
                    k=a[0][i];
                    a[0][i]=a[0][i+1];
                    a[0][i+1]=k;
                    k=a[1][i];
                    a[1][i]=a[1][i+1];
                    a[1][i+1]=k;
                }
            }
        }
}
//ͳ��������е�Ԫ�ظ���
type orderedlist(int n,type *list)
{
    int i,count=1,maxcount=1;
    type value;
    for(i=0;i<(n-1);i++) {
        if(list[i]!=list[i+1]) {
            //printf("count of %d is value %d\n",list[i],count);
            if(count>maxcount){
                maxcount=count;
                value=list[i];
                count=1;
            }
        }
        else
            count++;
    }
    if(count>maxcount){
            maxcount=count;
            value=list[n-1];
    }
    //printf("value %f has a Maxcount:%d\n",value,maxcount);
    return value;
}

int main()
{
    int i,j,k;
    int D,N;    //ά�ȣ�������
    type **array=NULL;  //��������
    type **karray=NULL; //  K���ڵ�ľ��뼰���ǩ
    type *testdata; //��������
    type dist,maxdist;

    loaddata(&N,&D,&array,&karray);
    testdata=(type *)malloc((D-1)*sizeof(type));
    printf("input test data containing %d numbers:\n",D-1);
    for(i=0;i<(D-1);i++)    scanf("%f",&testdata[i]);

    while(1){
    for(i=0;i<K;i++){
        if(K>N) exit(-1);
        karray[0][i]=computedistance(D-1,testdata,array[i]);
        karray[1][i]=array[i][D-1];
        //printf("first karray:%6.2f  %6.0f\n",karray[0][i],karray[1][i]);
    }

    bublesort(K,karray,0);
    //for(i=0;i<K;i++)    printf("after bublesort in first karray:%6.2f  %6.0f\n",karray[0][i],karray[1][i]);
    maxdist=karray[0][K-1]; //��ʼ��k��������ľ������ֵ

    for(i=K;i<N;i++){
        dist=computedistance(D-1,testdata,array[i]);
        if(dist<maxdist)
            for(j=0;j<K;j++){
                if(dist<karray[0][j]){
                    for(k=K-1;k>j;k--){ //j��Ԫ�ظ��Ƶ���һλ��Ϊ������׼��
                        karray[0][k]=karray[0][k-1];
                        karray[1][k]=karray[1][k-1];
                    }
                    karray[0][j]=dist;  //���뵽jλ��
                    karray[1][j]=array[i][D-1];
                    //printf("i:%d  karray:%6.2f %6.0f\n",i,karray[0][j],karray[1][j]);
                    break;  //���Ƚ�karray����Ԫ��
                }
            }
        maxdist=karray[0][K-1];
        //printf("i:%d  maxdist:%6.2f\n",i,maxdist);
    }
    //for(i=0;i<K;i++)    printf("karray��%6.2f  %6.0f\n",karray[0][i],karray[1][i]);
    bublesort(K,karray,1);
    //for(i=0;i<K;i++)    printf("after bublesort in karray��%6.2f  %6.0f\n",karray[0][i],karray[1][i]);
    printf("\nThe data has a tag: %.0f\n\n",orderedlist(K,karray[1]));

    printf("input test data containing %d numbers:\n",D-1);
    for(i=0;i<(D-1);i++)    scanf("%f",&testdata[i]);
    }
    return 0;
}







