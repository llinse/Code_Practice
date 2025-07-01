### **Map结构的实现**

>  Map ：“键值”对映射的抽象接口。该映射不包括重复的键，一个键对应一个值。 
>
>  （基于二叉树实现）



#### 实现要求

```java
int size();
/*返回这个Map中所包含的键值对的数量，如果大于Integer.MAX_VALUE，则应该返回Integer.MAX_VALUE。*/

boolean isEmpty();
/*检测Map是否为空*/

void clear();
/*删除Map中所有的键值对。*/

V put(K key, V value);
/**
 * 添加一对键值对，如果Map中已含有这个key，那么新value将覆盖掉旧value，
 * 并返回旧value，如果Map中之前没有这个key，那么返回null。
 */

V get(K key);
/*根据key查找value，如果Map不包含该key，则返回null。*/

V remove(K key);
/*删除指定key并返回之前的value，如果Map中没有该key，则返回null。*/

boolean containsKey(K key);
/*Map中是否包含key，如果是返回true，否则false。*/

boolean containsValue(V value);
/*Map中是否包含value，如果是返回true，否则false。*/

void traversal(map.Visitor<K, V> visitor);
/*根据用户提供的visitor进行遍历*/
```



#### 初始定义

```java
private Node root;
private int size;

public map(){
    root = null;
    size = 0;
}
```



```java
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
```



#### size功能的实现

```java
public int size() {
        return size;
    }
```



#### is Empty功能的实现

```java
public boolean isEmpty() {
        return size == 0;
    }
```



#### clear功能实现

```java
public void clear() {
        root = null;
        size = 0;
    }
```



#### put功能的实现

```java
private Node getKey(Node node, K key){
        if (node == null) return null;

        if (key.compareTo(node.key) < 0) return getKey(node.left, key);
        else if (key.compareTo(node.key) > 0) return getKey(node.right, key);
        else return node;
    }

private Node getValue(Node node, V value){
        if (node == null) return null;

        if (value.compareTo(node.value) < 0) return getValue(node.left, value);
        else if (value.compareTo(node.value) > 0) return getValue(node.right, value);
        else return node;
    }

// put功能的实现
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
    
        return node;
    }
```



#### get功能的实现

```java
public V get(K key){
        Node node = getKey(root, key);
        return node == null ? null : node.value;
    }
```



#### remove功能的实现

```java
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
```



#### contains Key功能的实现

```java
public boolean containsKey(K key) {
        return getKey(root, key) != null;
    }
```



#### contains Value功能的实现

```java
public boolean containsValue(V value) {
        return getValue(root, value) != null;
    }
```



#### traversal功能的实现

```java
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
```

