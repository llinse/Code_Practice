public class map<K extends Comparable<K>, V extends Comparable<V>> implements mapMethods<K,V> {
    
    // 基于二叉搜索树的map实现
    private Node root;
    private int size;

    // 初始化
    public map(){
        root = null;
        size = 0;
    }

    // 每个键值对作为一个Node对象
    private class Node{
        public K key;
        public V value;
        public Node left, right;

        public Node(K key, V value){
            this.key = key;
            this.value = value;
            left = null;
            right = null;
        }
    }

    // size功能的实现
    @Override
    public int size() {
        return size;
    }

    // isEmpty功能的实现
    @Override
    public boolean isEmpty() {
        return size == 0;
    }

    // clear功能的实现
    @Override
    public void clear() {
        root = null;
        size = 0;
    }

    // 递归查找，获取以node为根节点的BST中key所在的节点
    private Node getKey(Node node, K key){
        if (node == null) return null;

        if (key.compareTo(node.key) < 0) return getKey(node.left, key);
        else if (key.compareTo(node.key) > 0) return getKey(node.right, key);
        else return node;
    }

    // 递归查找，获取以node为根节点的BST中value所在的节点
    private Node getValue(Node node, V value){
        if (node == null) return null;

        if (value.compareTo(node.value) < 0) return getValue(node.left, value);
        else if (value.compareTo(node.value) > 0) return getValue(node.right, value);
        else return node;
    }

    // put功能的实现
    @Override
    public V put(K key, V value) {
        Node node = getKey(root, key);

        if(node == null) {  // 插入原本没有的键
            root = put(root, key, value); 
            return null;
        } else {  // 插入原本就有的键
            V old = node.value;
            node.value = value;
            return old;
        }
    }

    // 以node为根递归插入元素(key, value)
    private Node put(Node node, K key, V value){
        if (node == null) {
            size ++;
            return new Node(key, value);
        }

        if (key.compareTo(node.key) < 0)
            node.left = put(node.left, key, value);
        else if (key.compareTo(node.key) > 0)
            node.right = put(node.right, key, value);
        else
            node.value = value;

        // 返回插入新节点后BST的根
        return node;
    }

    // get功能的实现
    @Override
    public V get(K key){
        Node node = getKey(root, key);
        return node == null ? null : node.value;
    }

    // remove功能的实现
    @Override
    public V remove(K key) {
        Node node = getKey(root, key);
        if (node != null) {  // 找到了这个key
            root = remove(root, key);
            return node.value;
        }
        // 没找到直接返回空
        return null;
    }

    private Node remove(Node node, K key){
        if (node == null)
            return null;

        if (key.compareTo(node.key) < 0) {
            node.left = remove(node.left , key);
            return node;
        } else if (key.compareTo(node.key) > 0) {
            node.right = remove(node.right, key);
            return node;
        } else{
            // 待删除节点左子树为空
            if(node.left == null){
                Node rightNode = node.right;
                node.right = null;
                size --;
                return rightNode;
            }
            // 待删除节点右子树为空
            if(node.right == null){
                Node leftNode = node.left;
                node.left = null;
                size --;
                return leftNode;
            }
            // 待删除节点左右子树均不为空的情况
            // 找到待删除节点后继节点代替待删除节点
            Node successor = successor(node.right);
            successor.right = removeSuc(node.right);
            successor.left = node.left;
            node.left = node.right = null;

            return successor;
        }
    }

    private Node successor(Node node){
        if(node.left == null)
            return node;
        return successor(node.left);
    }

    // 删除以node为根的BST中的最小节点
    private Node removeSuc(Node node){
        if (node.left == null) {
            Node rightNode = node.right;
            node.right = null;
            size --;
            return rightNode;
        }

        node.left = removeSuc(node.left);
        return node;
    }

    // containsKey功能的实现
    @Override
    public boolean containsKey(K key) {
        return getKey(root, key) != null;
    }

    // containsValue功能的实现
    @Override
    public boolean containsValue(V value) {
        return getValue(root, value) != null;
    }

    // traversal功能的实现
    @Override
    public void traversal(Visitor<K,V> visitor) {
        if (visitor == null) return;
        traversal(root, visitor);
    }

    private void traversal(Node root, Visitor<K,V> visitor) {
        // 递归的退出条件
        if (root == null || visitor.stop) return;

        // 中序遍历左子树
        traversal(root.left, visitor);
        // 一旦满足visitor中定义的停止条件就return
        if (visitor.stop) return;
        // 访问根节点
        visitor.stop = visitor.visit(root.key, root.value);
        // 中序遍历右子树
        traversal(root.right, visitor);
    }

    // 外部访问Visitor
    public static abstract class Visitor<K,V> {
        private boolean stop;
        // 如果返回值是true，就马上停止遍历
        public abstract boolean visit(K key, V value);
    }

    // 按中序遍历打印map
    public void print() {
        System.out.print("{");
        print(root);
        System.out.println("}");
    }

    public void print(Node root) {
        // 递归的退出条件
        if (root == null) return;

        // 中序遍历左子树
        print(root.left);
        // 访问根节点
        System.out.print(root.key + ": ");
        System.out.print(root.value + ", ");
        // 中序遍历右子树
        print(root.right);
    }
}
