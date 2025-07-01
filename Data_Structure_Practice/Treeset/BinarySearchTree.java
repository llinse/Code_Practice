public class BinarySearchTree{ 
    // 二叉搜索树类
    private class Node
    { // 节点类
        int data; // 数据域
        Node right; // 右子树
        Node left; // 左子树
    }

    private Node root; // 树根节点
    private int size;
    private int size1;
    private int size2;
    private boolean cons;

    // 初始化
    public BinarySearchTree(){
        root = null;
        size = 0;
        size1 = 0;
        size2 = 0;
    }

    // size功能的实现
    public int size() {
        size = size1 - size2;
        return size;
    }

    // isEmpty功能的实现
    public boolean isEmpty() {
        return size == 0;
    }

    // clear功能的实现
    public void clear() {
        root = null;
        size = 0;
    }


    // add函数的实现
    public void add(int key)
    {
        Node p = new Node(); // 待插入的节点
        p.data = key;

        size1++;
        
        if (root == null)
        {
            root = p;
        }
        else
        {
            Node parent = new Node();
            Node current = root;
            while (true)
            {
                parent = current;
                if (key > current.data)
                {
                    current = current.right; // 右子树
                    
                    if (current == null)
                    {
                        parent.right = p;
                        return;
                    }
                }
                else if (key < current.data)
                {
                    current = current.left; // 左子树
                    if (current == null)
                    {
                        parent.left = p;
                        return;
                    }
                }
                else
                {
                    size2++;
                    return;
                }
            }
        }
    }
    
    

    /*traversal函数的实现*/
    public void preOrder(Node root)
    { // 前序遍历,"中左右"
        if (root != null)
        {
            System.out.print(root.data + " ");
            preOrder(root.left);
            preOrder(root.right);
        }
    }

    public void inOrder(Node root)
    { // 中序遍历,"左中右"
        if (root != null)
        {
            inOrder(root.left);
            System.out.print(root.data + " ");
            inOrder(root.right);
        }
    }

    public void traversal(int traverseType)
    { // 选择以何种方式遍历
        switch (traverseType)
        {
        case 1:
            System.out.print("preOrder traversal: ");
            preOrder(root);
            System.out.println();
            break;
        case 2:
            System.out.print("inOrder traversal: ");
            inOrder(root);
            System.out.println();
            break;
        }
    }



    public Node find(int key)
    { // 从树中按照关键值查找元素
        Node current = root;
        while (current.data != key)
        {
            if (key > current.data)
                current = current.right;
            else
                current = current.left;
            if (current == null) return null;
        }
        return current;
    }
    
    // constains函数的实现
    public boolean constains(Node node)
    {    //输出节点的数据域
        if(node!=null){
            System.out.println("True");
            cons = true;
            return cons;
        }
        else{
            System.out.println("False");
            cons = false;
            return cons;
        }
    }
    
    
    
    private Node getSuccessor(Node delNode)    //寻找要删除节点的中序后继结点
    {
        Node successorParent=delNode;
        Node successor=delNode;
        Node current=delNode.right;
        
        //用来寻找后继结点
        while(current!=null)
        {
            successorParent=successor;
            successor=current;
            current=current.left;
        }
        
        //如果后继结点为要删除结点的右子树的左子，需要预先调整一下要删除结点的右子树
        if(successor!=delNode.right)
        {
            successorParent.left=successor.right;
            successor.right=delNode.right;
        }
        return successor;
    }
    
    
    /*remove函数的实现 */
    public boolean remove(int key) // 删除结点
    {
        size2++;
        Node current = root;
        Node parent = new Node();
        boolean isRightChild = true;
        while (current.data != key)
        {
            parent = current;
            if (key > current.data)
            {
                current = current.right;
                isRightChild = true;
            }
            else
            {
                current = current.left;
                isRightChild = false;
            }
            if (current == null) return false; // 没有找到要删除的结点
        }
        // 此时current就是要删除的结点,parent为其父结点
        // 要删除结点为叶子结点
        if (current.right == null && current.left == null) 
        {
            if (current == root)
            {
                root = null; // 整棵树清空
            }
            else
            {
                if (isRightChild)
                    parent.right = null;
                else
                    parent.left = null;
            }
            return true;
        }
        //要删除结点有一个子结点
        else if(current.left==null)
        {
            if(current==root)
                root=current.right;
            else if(isRightChild)
                parent.right=current.right;
            else
                parent.left=current.right;
            return true;
        }
        else if(current.right==null)
        {
            if(current==root)
                root=current.left;
            else if(isRightChild)
                parent.right=current.left;
            else
                parent.left=current.left;
            return true;
        }
        //要删除结点有两个子结点
        else 
        {
            Node successor=getSuccessor(current);    //找到要删除结点的后继结点
            
            if(current==root)
                root=successor;
            else if(isRightChild)
                parent.right=successor;
            else
                parent.left=successor;
            
            successor.left=current.left;
            return true;
        }
    }
}
