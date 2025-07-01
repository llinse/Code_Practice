public interface mapMethods<K,V> {

    int size();
    /*返回这个Map中所包含的键值对的数量*/
    
    boolean isEmpty();
    /*检测Map是否为空*/
    
    void clear();
    /*删除Map中所有的键值对*/
    
    V put(K key, V value);
    /**
     * 添加一对键值对，如果Map中已含有这个key，那么新value将覆盖掉旧value，
     * 并返回旧value，如果Map中之前没有这个key，那么返回null。
     */
    
    V get(K key);
    /*根据key查找value，如果Map不包含该key，则返回null*/
    
    V remove(K key);
    /*删除指定key并返回之前的value，如果Map中没有该key，则返回null*/
    
    boolean containsKey(K key);
    /*Map中是否包含key，如果是返回true，否则false*/
    
    boolean containsValue(V value);
    /*Map中是否包含value，如果是返回true，否则false*/
    
    void traversal(map.Visitor<K, V> visitor);
    /*根据用户提供的visitor进行遍历*/
}
