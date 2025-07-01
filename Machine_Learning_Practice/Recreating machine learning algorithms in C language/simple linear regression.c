#include <stdio.h>
#include <stdlib.h>
 
int main()
{
    float x[5]={1.0,1.0,4.0,3.0,5.0};
    float y[5]={1.0,3.0,3.0,2.0,5.0};
		
		int n; 
	  n = sizeof(x) / sizeof(x[0]);
 
    float B0,B1,x,y,sum_x,sum_y,mean_x,mean_y,var_x,var_y,cov;
    int i;
		
    B0=B1=x=y=sum_x=sum_y=mean_x=mean_y=var_x=var_y=cov=0.0;
 
    for(i=0;i<n;i++)
    {
        sum_x=1.0*x[i]+sum_x;
        sum_y=1.0*y[i]+sum_y;
    }
		
		mean_x=sum_x/n;
		mean_y=sum_y/n;
		
		for(i=0;i<n;i++)
    {
        var_x=(1.0*x[i]-mean_x)**2+var_x;
        var_y=(1.0*y[i]-mean_y)**2+var_y;
    }
		
		for(i=0;i<n;i++)
    {
        cov=(x[i]-mean_x)*(y[i]-mean_y)+cov;
    }
 
    B1=1.0*cov/var_x;
    B0=1.0*mean_y-B1*mean_x;
 
    printf("Y=%0.2fx+%0.2f\n",B1,B0);
    
    system("pause");
    return 0;
}