    public class Main {
    public static void main(String[] args) {
        map<String, Integer> person = new map<>();

        person.put("Amy",60);
        person.put("Bob",70);
        person.put("Coco",80);
        person.put("Dave",90);


        /*put功能的实现*/
        // 如果键不存在，实现添加，无返回
        person.put("Even",95);
        person.print();

        // 如果键存在，覆盖原值并返回
        System.out.println(person.put("Amy",66));
        person.print();

        /*get功能的实现*/
        System.out.println(person.get("Bob"));

        /*containsKey功能的实现*/
        System.out.println(person.containsKey("John"));

        /*containsValue功能的实现*/
        System.out.println(person.containsValue(95));

        /*traversal功能的实现*/
        person.traversal(new map.Visitor<String, Integer>() {
            public boolean visit(String key, Integer value) {
                System.out.println(key + "同学的成绩是："+ value);
                return false;
            }
        });


        /*size功能的实现*/
        System.out.println("\n元素个数: "+person.size());
        
        /*remove功能的实现*/
        person.remove("Amy");
        System.out.println("\n删除后的元素个数: "+person.size());
        test(!person.containsKey("Amy"));
        
        /*isEmpty功能的实现*/
        test(!person.isEmpty());

        /*clear功能的实现*/
        person.clear();
        test(person.isEmpty());
    }

    // 断言测试代码
    public static void test(boolean v) {
        if (v) return;
        System.err.println(new RuntimeException().getStackTrace()[1]);
    }
}