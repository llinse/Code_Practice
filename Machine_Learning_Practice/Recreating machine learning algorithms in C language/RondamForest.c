#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <ctime>
#include <algorithm>
#include <string.h>
#include <stdio.h>

#define N 999 //三位小数。

using namespace std;

typedef vector<int> vec;

const int maxF = 100000;

const int n_T = 10;
const int n_I = 1000;   // 行采样个数
const string out = "result.txt";  //文件内容自定义
const string T = "test.txt";
const string re = "result.txt";

 

vector < vector <double> > TrainData; 
vector < vector <double> > TestData;
vector < vector <double> > fTestData;
vector <double> TestLable;
vector <double> values_tlable;
vector <double> lable;         //统计values_lable ,
vector <double> values_lable;
vector <int> midR;

vector<double> errOOB1(n_T);//一棵树一个值



int	depth = 0;             //节点深度
int r, c;
int testnum=0;
int flag_leaf = 0;

int n_lable;
int n_tlable;

char ch;

//节点结构体
struct Node
{
	int Feature;   //划分子节点的bestF
	double FeatureValue;
	vector <Node *> ChildNodes;
	double Attribute;
}*Root;


//得到文件中矩阵行列数

 void GetSize(const string filename) //计算数据大小
 {
     ifstream file(filename);
	 if(!file)
	{
		printf("The file is not exist!");
		
	}

	if(file.eof())
	{
		printf("The file is empty!");
		
	}

	 int buf_size=0xfffff,witch=0;
	 char * buffer=new char[buf_size];
	 char * ptr;
	 char * delimiters=" ";
	 r=0;
	 c=0;
	 if (file.getline(buffer,buf_size,'\n' )!=NULL)
	 {
		++r;
		int l = strlen(buffer);
		for(int i = 0; i<l;i++)
		{
			if(buffer[i]==' ')
				c++;
		}
		/*while (ptr !=NULL)
		{
			++c;
			ptr = strtok (NULL, delimiters);
		}*/
	 } 

	 while(!file.eof())
	 {		 
		 if (file.getline(buffer,buf_size,'\n' )!=NULL)
		 { 
			++r;
		 }
	 }
	 
	 delete[] buffer,ptr;
	 file.clear();
	 file.close();


  }

	
//从文件读入数据
int input(string filename,vector < vector < double > > &DataSet,int row,int col)
{
	ifstream file_in(filename);
	
	if(!file_in)
	{
		printf("The file is not exist!");
		return -1;
	}

	if(file_in.eof())
	{
		printf("The file is empty!");
		return -1;
	}

	else
	{
		vector <double> empty;
		double temp;
		for(int i = 0; i < row; i++)
		{
			DataSet.push_back(empty);  
			for(int j = 0; j < col; j++) 
			{
				file_in >> temp;
				DataSet[i].push_back(temp);
			}	
		}
	}
	file_in.clear();
	file_in.close();
}


//输出结果到文件
void output(const string filename, int TestLable)
{

	ofstream outfile(filename, ofstream ::app);
	outfile << TestLable <<" ";
}

//采样序号
 vec Sample(int sampleI[n_I], int sampleF[maxF] ,int r,int c,int n_F)
{
	vector<int> s(r,0);
	vector<int> sampleT;
	static bool first=true;
	if(first)
	{
	///srand(time(0));
	srand((unsigned)time(NULL)); 
	first=false;
	}
	
    for(int i = 0; i < n_I; i++) 
	{
		sampleI[i] = rand()%r;   //有放回的随机抽取对象
		s[sampleI[i]]++;
		//cout << sampleI[i] << " ";//输出选择了哪几个样本
	}
	//cout << endl;
	cout<<"随机有放回的抽取"<<r<<"个样本\n"<<endl;//test
	testnum=0;

	for(int i=0;i<r;i++)//得到袋外数据集
	{
		if(s[i]==0)
		{
			sampleT.push_back(i);
			testnum++;
		}
	}
	printf("OOBset.size=%d\n",testnum);//test
	printf("n_F=%d\n",n_F);//test

	for(int i = 0; i != c-1; i++) sampleF[i] = i;     //随机抽取特征
    random_shuffle(sampleF,sampleF+(c-1));
	//for(int i = 0; i != n_F; i++) cout << sampleF[i] << " ";//输出选择了哪几个特征
	//cout << endl;

	return sampleT;//返回袋外数据集的序号
}

//获得vector中出现的所有值
void GetValues( vector<double> ObjectColumn , vector <double> &Values)
{
	vector <double> temp_vec(ObjectColumn);

	int temp = 0;
	while(!temp_vec.empty())
	{      
		Values.push_back(temp_vec[0]);
		for(vector<double>::iterator it = temp_vec.begin(); it != temp_vec.end(); )
		{
			if( *it ==Values[temp] )
				it = temp_vec.erase(it);
			else
				it++;
		}
		temp++;
	}
	temp_vec.clear();
}

//熵计算
double ComputeEntropy(vector< vector<int> > L_F)
	{
		int nc = L_F[0].size();
		int nr = L_F.size();

		double E = 10^10;
		for( int i = 0; i <nr; i++)
		{
			double sum = 0;
			for( int j = 0; j < nc; j++)
				sum = sum + L_F[i][j];
			//int sum = accumulate(lable_F[i].begin, lable_F[i].end, 0.0,);
			for( int j = 0; j < nc; j++)
			{
				if ((L_F[i][j] != 0) && (L_F[i][j] != sum))
					E += -( (double)(L_F[i][j]/sum)) * log10 ( (double)(L_F[i][j]/sum));
				else
					E += 0;
			}
		}
		return E;
	}

//确定节点BestFeature
int ChoseNodeFeature(vector < vector <double> > AllData, vector <double> LableSet, vector <double>LableValue, vector <int> Ibox, vector <int> &Fbox)
{

	int bestF = Fbox[0];
	int bestN = 0;
	double InitE;
	double gain = 0;
	double mid = 0;
	int n_LableValue = LableValue.size();
	//初始信息熵
	vector< vector<int> > lable_TJ;       //未按属性分类的不同类别的统计表
	vector <int> empty (n_LableValue,0);
	lable_TJ.push_back(empty);
	for (int i = 0; i < Ibox.size(); i++)
	{
		for(int j = 0; j < n_LableValue; j++)
						{
							if( LableValue[j]  == LableSet[Ibox[i]])
								lable_TJ[0][j] = lable_TJ[0][j] + 1;
						}	
	}

	InitE = ComputeEntropy(lable_TJ);
	//各属性分类后的信息熵
	for(int i = 0; i < Fbox.size(); i++)
	{
		vector<double> temp_F;  
		vector<double> temp_L;
		vector<int> empty(n_LableValue,0);
		vector< vector<int> > lable_F;
		
		for(int j = 0; j != Ibox.size(); j++)       //临时存储第一个特征行
			temp_F.push_back(AllData[Ibox[j]][Fbox[i]]);
	
		for(int j = 0; j != Ibox.size(); j++)       //临时存储特征lable
			temp_L.push_back(LableSet[Ibox[j]]);
	
		int temp = 0;
		while(!temp_F.empty())     
		{   
	       
			lable_F.push_back(empty);
			int LL = 0;
			double FF = temp_F[0];
			for(vector<double>::iterator it = temp_F.begin(); it != temp_F.end(); )
				{ // 一个循环完成只是对某一行的某一个值完成了一次扫描
					if( *it == FF )
					{   //对*it的值进行lable判断

						for(int k = 0; k < n_LableValue; k++)
						{
							if( LableValue[k]  == temp_L[LL])
								lable_F[temp][k] = lable_F[temp][k] + 1;
						}
						it = temp_F.erase(it);
						temp_L.erase(temp_L.begin() + LL);
					}
					else
					{
						it++;
						LL++;
					}
				}	
			temp++;
		}
		temp_F.clear();  //以上得到一个lable_F某一特征的特征值及类别情况

		//信息增益
		mid = InitE-ComputeEntropy(lable_F);

		if(mid >= gain)
		{
			gain = mid;
			bestF = Fbox[i];
			bestN = i;
		}	
	}
	//updatFset
	Fbox.erase(Fbox.begin() + bestN);

	//cout<<"返回的特征："<<bestF<<endl;//test

	return  bestF; //返回实际第几个特征
}
	//判断是否继续划分
	// 1.SubSet是否为空 --根据FeaturesValue得到子集故不可能为空
	// 2.所有对象是否属于一个类别
	bool SameAttribute( vector <int> SubSet, vector <double> LableSet )
	{
       int count = 0;
	   for( int i = 0; i < SubSet.size(); i++)
	   {
		   
			if(LableSet[SubSet[i]] == LableSet[SubSet[0]])
					count ++;
	   }

	   if( count == SubSet.size())
		   return true;
	   else
		   return false;
	}

	// 3.F_box是否为空
	bool EmptyFeatureSet(vector <int> Fbox)
	{
		if( Fbox.size() == 0)
			return true;
		else
			return false;
	}
	//4. 属性值为空后投票决定叶子节点属性
	double VoteAttribute( vector <int> NodeSet, vector <double> LableSet ,vector <double> LableValue)
	{
		int temp = 0;
		int max = 0;
		double maxAttribute;
		for(int i = 0; i < LableValue.size();i++)
		{
			for( int j = 0; j < NodeSet.size(); j++ )
			{
				if ( LableSet[NodeSet[j]] == LableValue[i])
					temp++;
			}
			if (temp >= max)
			{
				max = temp;
				maxAttribute = LableValue[i];
			}
		}
		return maxAttribute;
	}


//构建树
Node* BuildDT(Node * p,vector <int> NodeData,vector <double> Lable, vector <double> LableValue, vector <int> Fbox,vector < vector <double> > AllData,int n_F)
{
	int i = 0 ;
	int j = 0 ;
	//printf("n_F=%d\n",n_F);//test
	if( p == NULL )
		p = new Node();

	if( SameAttribute(NodeData,Lable) == true )
	{   
		p-> Attribute = Lable[NodeData[0]];
	}
		
	else
	{ 
		if( EmptyFeatureSet(Fbox) == true)
			p-> Attribute = VoteAttribute(NodeData,Lable,LableValue);
		else
		{
			//确定节点的Feature
			int ChosenFeature = ChoseNodeFeature(AllData, Lable, LableValue, NodeData, Fbox); 
			p-> Feature = ChosenFeature;
			cout<<"确定为节点的Fearure："<<ChosenFeature<<endl;//test

			//获得Feature的特征值
			vector <double> Feature; 
			vector <double> FeatureValue;
			printf("NodeData.size()=%d\n",NodeData.size());//test
			for(int i = 0 ; i < NodeData.size() ; i++)
				Feature.push_back(AllData[NodeData[i]][ChosenFeature]);
			GetValues( Feature , FeatureValue );

			//根据特征值划分子集
			vector < vector<int> > SubSet (FeatureValue.size());
			vector <int> empty;

			printf("FeatureValue.size()=%d\n",FeatureValue.size());//test

			for( i = 0 ; i < FeatureValue.size() ; i++)
			{
				SubSet.push_back(empty);
	    
				for( j = 0 ; j < NodeData.size() ; j++)
				{
					if(Feature[j] == FeatureValue[i])
					{
						SubSet[i].push_back(NodeData[j]);
					}
				}
				
				//递归函数返回时即回溯时需要1 将新结点加入父节点孩子容器 2清除new_state容器
				vector <int> NewNodeSet (SubSet[i]);   //下一级节点
				Node *Child_Node = new Node();
				
				p -> ChildNodes.push_back(Child_Node);    //存储子节点地址
				
				Child_Node ->FeatureValue = FeatureValue[i];  //向下推特征值
				
				/*Feature.clear();
				vector <double>(Feature).swap(Feature);
				cout << "Feature Vector 的 容量为" << Feature.capacity() << endl;
				FeatureValue.clear();
				vector <double>(FeatureValue).swap(FeatureValue);
				cout << "FeatureValue Vector 的 容量为" << FeatureValue.capacity() << endl;
				SubSet.clear();
				vector < vector<int> >(SubSet).swap(SubSet);
				cout << "SubSet Vector 的 容量为" << SubSet.capacity() << endl;
				empty.clear();
				vector <int>(empty).swap(empty);
				cout << "empty Vector 的 容量为" << empty.capacity() << endl;*/

				//cin >> ch;// 检查内存情况

				depth = n_F - Fbox.size();
				//cout<<"depth="<<depth<<endl;//test
				BuildDT(Child_Node,NewNodeSet, Lable, LableValue, Fbox, AllData,n_F);
		    
			
				NewNodeSet.clear();
			}
		}

	}
		
	return p;
}

//打印树
void PrintTree(Node *p, int depth){
	for (int i = 0; i < depth; i++) cout << '\t';//按照树的深度先输出tab  ??

	if(p-> FeatureValue != NULL)//不为根节点
	{
		cout<< p->FeatureValue<<endl;
		for (int i = 0; i < depth+1; i++) cout << '\t';//按照树的深度先输出tab
	}
	if(p->ChildNodes.empty())//为叶子节点
	{
		cout<< p->Attribute<<endl;
		for (int i = 0; i < depth+1; i++) cout << '\t';//按照树的深度先输出tab
	}
	if(!p->ChildNodes.empty())//为叶子节点
		cout<<p->Feature<<endl;
	else 
		cout<<"leaf"<<endl;
	for (vector<Node*>::iterator it = p->ChildNodes.begin(); it != p->ChildNodes.end(); it++){
		PrintTree(*it, depth + 1);
	}
}

//释放内存
void Free(Node* p)
{
	if (p == NULL)
		return;
	
	for(vector<Node*> ::iterator it = p-> ChildNodes.begin(); it < p->ChildNodes.end(); it++)
		Free(*it);
	delete p;


}

//分类器
void ClassT(Node* p, vector<double>TestItem, vector <int> &mid,int &flag_leaf)
{
	flag_leaf = 0;
	if(p->ChildNodes.size() == NULL)//判断是否进入叶子节点
	{
		flag_leaf = 1;
		cout << "进入叶子节点 " <<"data's attributr is "<< p-> Attribute<<endl;
		mid.push_back(p->Attribute);
		//output(out,p-> Attribute);

	}
		
	else
	{
		for(vector<Node*> ::iterator it = p-> ChildNodes.begin(); it < p->ChildNodes.end(); it++)
		{
			if( (*it)->FeatureValue == TestItem[p->Feature])
				ClassT(*it,TestItem,mid,flag_leaf);	
			
		}	

		/*for(int i = 0; i <  p-> ChildNodes.size(); i++) //效果同上
		{
			if( (p-> ChildNodes[i])->FeatureValue == TestData[p->Feature])
				Classifier((p-> ChildNodes[i]),TestData);	
		}*/	
	}

}
void Classifier(Node* p, vector<double>TestItem, vector <int> &mid,int n_lable,int &flag_leaf)
{
	ClassT(p,TestItem, mid,flag_leaf);
	if(flag_leaf != 1)
	{
		int randlable =rand()%n_lable;
		mid.push_back(randlable);
		cout <<"未进入子节点  random attribute = "<<randlable <<endl;
	}                                                   
}

void exit_with_help()
{
	printf(
	"Usage: C_RForest.exe input_file output_file n_F FNum\n"
	"eg:Input_TXT E:\\sample\\sumresult_emb100\\汉男\\RFpsig.txt\n"
	"eg:Output_TXT E:\\sample\\sumresult_emb100\\汉男\\psigSVM_RForest_result.txt\n"
	"eg:Modelput_TXT E:\\sunjun\\FS\\psig100Medol.txt\n"
	"n_F: 特征选取集的大小\n"
	"FNum : 降维后的特征维度\n"
	);
	exit(1);
}
//int main(char * Input_TXT,char * Output_TXT,string in,int FNum,int n_F)
int main(int argc, char **argv)
{
	    int errNum=0;
		string in;	
		char Input_TXT[200];
		char Output_TXT[200];
		char Modelput_TXT[200];

		//in=argv[1];
		//sprintf(Input_TXT,"%s",argv[1]);
		//printf("%s\n",Input_TXT);//test
		//sprintf(Output_TXT,"%s",argv[2]);
		//printf("%s\n",Output_TXT);//test
		//sprintf(Modelput_TXT,"%s",argv[3]);
		//printf("%s\n",Modelput_TXT);//test
		//int n_F;
		//n_F=atoi(argv[4]);
		//printf("n_F=%d\n",n_F);//test
		//int FNum;
		//FNum = atoi(argv[5]);
		//printf("FNum=%d\n",FNum);//test

		//test
		in="E:\\sample\\sumresult_emb10\\汉女\\RFpsig.txt";//test
		sprintf(Input_TXT,"E:\\sample\\sumresult_emb10\\汉女\\RFpsig.txt");
		printf("%s\n",Input_TXT);//test
		sprintf(Output_TXT,"E:\\sample\\sumresult_emb10\\汉女\\psigSVM_RForest_result.txt");
		printf("%s\n",Output_TXT);//test
		sprintf(Modelput_TXT,"E:\\sunjun\\FS\\ZGpsig10Medol.txt");
		printf("%s\n",Modelput_TXT);//test
		int n_F=26;
		printf("n_F=%d\n",n_F);//test
		int FNum=10;
		printf("FNum=%d\n",FNum);//test
		//test

		GetSize(in); //计算数据大小
		
		cout<<"***row="<<r<<"***\n"<<"***col="<<c<<"***\n"<<endl;//test

		vector<vector<double>> errOOB2(n_T,vector<double>(c));

		const int row = r;
		const int col = c;
		
		FILE *Ifp = NULL;
		FILE *Ofp = NULL;
		FILE *mOfp = NULL;

		TrainData.clear();
		input(in,TrainData,row,col); 

		//lable.clear();
		//values_lable.clear();
		for(int j = 0; j != r;j++)
		{
			//printf("TrainData[%d][%d]=%lf\n",j,c-1,TrainData[j][c-1]);//test
			lable.push_back(TrainData[j][c-1]);
		}
		GetValues(lable, values_lable);
		n_lable = values_lable.size();
		cout<<"n_lable="<<n_lable<<"\n"<<endl;//test
		

	srand((unsigned)time(NULL)); 

	for(int e = 0; e < n_T; e++)
	{
		int I[n_I];   //采样序号集
		int F[maxF];   //200为特征数上界  若大于只要改下200
		vector<int> T;
		T.clear();
		T = Sample(I, F,row,col,n_F);

		vector <int> II(I, I + n_I);
		vector <int> FF(F, F + n_F);  
		

		Root = NULL;
		Root = BuildDT(Root,II,lable, values_lable, FF,TrainData,n_F);

		II.clear();
		FF.clear();

		printf("[---print the %d tree\n",e);//test
	
		PrintTree(Root,0);

		printf("printed the %d tree---]\n",e);//test

		TestData.clear();
		fTestData.clear();
		TestLable.clear();

		//printf("0:*****\n");//test

		for(int j = 0; j != testnum;j++)
		{
			TestData.push_back(TrainData[T[j]]);
			TestLable.push_back(TestData[j][c-1]);
		}

		errNum=0;
		//printf("1:*****\n");//test
		for(int i = 0;i != testnum;i++)
		{
			Classifier(Root,TestData[i],midR,n_lable,flag_leaf);//当前只对一个数据进行分类
			if(midR[i]!=TestLable[i])
				errNum++;
		}
		printf("1:errNum=%d\n",errNum);//test
		printf("no.%d tree's OOB error rate=%lf\n",e,(double)errNum/testnum);//test
		errOOB1[e]=(double)errNum/testnum;
		printf("errOOB1[%d]=%lf\n",e,errOOB1[e]);//test

		for(int i=0;i<c;i++)
		{
			midR.clear();
			errNum=0;
			fTestData=TestData;
			printf("fTestData.size=%d\n",fTestData.size());//test
			//printf("3:*****\n");//test
			for(int j=0;j<testnum;j++)
				fTestData[j][i]=rand()%(N+1)/(float)(N+1);
			for(int k = 0;k != testnum;k++)
			{
				//printf("4:*****\n");//test
				Classifier(Root,fTestData[k],midR,n_lable,flag_leaf);//当前只对一个数据进行分类
				if(midR[k]!=TestLable[k])
					errNum++;
			}
			printf("2:errNum=%d\n",errNum);//test
			//printf("5:*****\n");//test
			double oobtemp=errOOB1[e]-(double)errNum/testnum;
			errOOB2[e][i]=oobtemp;
			printf("errOOB2[e][i]=%lf\n",errOOB2[e][i]);//test
			//system("pause");//test
		}
	
		Free(Root);

		//input(re,TrainData); 

	}
	

	vector<double> VI(c-1,0);

	for(int i=0;i<c-1;i++)
	{
		for(int j=0;j<n_T;j++)
		{
			VI[i]+=errOOB2[j][i];
		}
		VI[i]=VI[i]/n_T;
		printf("no.%d feature's importance value=%lf\n",i,VI[i]);//test
		
	}
	
	cout<<"对特征进行排序"<<endl;
	int *b;          //特征序号
	int i,j,k;
	b = (int*)malloc((c-1)*sizeof(int));
	for(i=0;i<c-1;i++)
	{
		b[i]=i;
	}
	double temp;
	for(i=0;i<c-2;i++)
	{
		for(j=i+1;j<c-1;j++)
		{
			if(VI[i]<VI[j])
			{
				temp = VI[i];
				VI[i] = VI[j];
				VI[j] = temp;

				temp = b[i];
				b[i] = b[j];
				b[j] = temp;
			}
		}
	}
	mOfp = fopen (Modelput_TXT,"w");
	for(i=0;i<c-1;i++)
	{
		cout<<i<<endl;
		cout<<b[i]<<" : "<<VI[i]<<"\n"<<endl;
		fprintf(mOfp,"%d ",b[i]);
	}
	fclose(mOfp);

	//输出降维后的样本集
	printf("c=%d",c);//test

	Ifp = fopen (Input_TXT,"r");
	printf("Input_TXT=%s\n",Input_TXT);
	if(Ifp==NULL)
	{
		printf("error\n");
		system("pause");
	}

	Ofp = fopen (Output_TXT,"w");
	printf("Output_TXT=%s\n",Output_TXT);
	if(Ofp==NULL)
	{
		printf("error\n");
		system("pause");
	}
	double dtemp = 0.0;
	double *ss;

	ss = (double*)malloc(c*sizeof(double));

	for(i=0;i<r;i++)
	{		
		for(j=0;j<c;j++)
		{
			fscanf(Ifp,"%lf",&ss[j]);
		}
		fprintf(Ofp,"%d ",(int)ss[c-1]);
		for(k=0;k<FNum;k++)
		{
			fprintf(Ofp,"%d:%lf ",k+1,ss[b[k]]);
		}
		fprintf(Ofp,"\n");
	}

	fclose(Ifp);
	fclose(Ofp);

	VI.clear();
	free(ss);
	free(b);
	//system("pause");
	return 0;

}
