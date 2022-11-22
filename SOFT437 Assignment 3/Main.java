public class Main {
    public static void main(String[] args) {
        Instrumentation ins = Instrumentation.Instance();
        ins.activate(true);
        //ins.testOverhead();
        Test.test(ins);
        ins.printLog();
        ins.dump(null);        
    }
}