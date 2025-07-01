public class Main
{
	public static void main(String[] args) 
	{
	    BinarySearchTree treeset = new BinarySearchTree();
        
        // add函数的测试
        // 通过添加函数的去重效果实现treeset的数据结构
        treeset.add(1);
        treeset.add(1);
        treeset.add(2);
        treeset.add(3);
        treeset.add(3);
        treeset.add(4);
        treeset.add(4);
        treeset.add(4);
        treeset.add(5);

        // traversal函数的测试
        treeset.traversal(1);
        treeset.traversal(2);
        
        // size函数的测试
        System.out.println(treeset.size());

        // constains函数的测试
        treeset.constains(treeset.find(2));
        treeset.constains(treeset.find(6));
        treeset.constains(treeset.find(4));
        
        // remove函数的测试
        treeset.remove(2);
        treeset.constains(treeset.find(2));
        System.out.println(treeset.size());
        
        // isEmpty函数的测试
        System.out.println(treeset.isEmpty());
        
        // clear函数的测试
        treeset.clear();
        System.out.println(treeset.isEmpty());

	}
}
