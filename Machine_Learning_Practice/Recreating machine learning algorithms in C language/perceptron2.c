#include <iostream>
#include <stdio.h>

double hypothose(double w[],int self_nin,double* inputs){
    double sum=0;
    for(int i=0;i<self_nin;i++){
        sum+=w[i]*inputs[i];
    }
    if (sum>0) return 1;
    else return 0;
}

void perceptron(int self_nin,int self_ndata,double a,int times,double** inputs,double w[]){
     int dimentions=self_nin+1;
     while(times--){
            double* delta_w=new double[self_nin];
            for(int i=0;i<self_nin;i++){
                delta_w[i]=0;
            }
            for(int i=0;i<self_ndata;i++){
                for(int j=0;j<self_nin;j++){
                    delta_w[j]+=(inputs[i][self_nin]-hypothose(w,self_nin,inputs[i]))*inputs[i][j]*a;
                }
            }
            for(int i=0;i<self_nin;i++){
                w[i]+=delta_w[i];
            }
            delete[] delta_w;
        }
}
int main(){
    int self_nin,self_ndata,times;
    double a;
    while(cin>>self_nin>>self_ndata>>a>>times){
        double** inputs=new double*[ self_ndata];
        for(int i=0;i<self_ndata;i++){
            inputs[i]=new double[self_ndata+2];
        }
        double* w=new double[self_nin+1];
        for(int i=0;i<self_ndata;i++){
            inputs[i][0]=1;
        }
        for(int i=0;i<self_ndata;i++){
            for(int j=1;j<=self_nin+1;j++){
                cin>>inputs[i][j];
            }
        }
        for(int i=0;i<=self_nin;i++){
            cin>>w[i];
        }
        perceptron(self_nin+1,self_ndata,a,times,inputs,w);
        for(int i=0;i<self_nin;i++){
            cout<<w[i]<<' ';
        }
        cout<<w[self_nin]<<endl;
        delete[] w;
        for(int i=0;i<self_ndata;i++){
            delete[] inputs[i];
        }
        delete[] inputs;
    }
    return 0;
}

