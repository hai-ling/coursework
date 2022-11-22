import java.util.Random;

class Test{
    static Instrumentation ins = null;
    private static int[] populateArray(int arraySize){
        int[] arr = new Random().ints(arraySize,1,99999).toArray();
        return arr;
    }

    private static void testBubbleSort(int arraySize, int numTimes){
        ins.comment("Measuring Bubble Sort");
        ins.startTiming(String.format("Random BubbleSort %d Times", numTimes));
        //ins.activate(false);
        for (int i = 0; i < numTimes; i++){
            int[] arr = populateArray(arraySize);
            BubbleSort.sort(arr);
        }
        //ins.activate(true);
        ins.stopTiming(String.format("Random BubbleSort %d Times", numTimes));
    }

    private static void testQuickSort(int arraySize, int numTimes){
        ins.comment("Measuring Quick Sort");
        ins.startTiming(String.format("Random QuickSort %d Times", numTimes));

        //ins.activate(false);
        for (int i = 0; i < numTimes; i++){
            int[] arr = populateArray(arraySize);
            QuickSort.sort(arr);
        }
        //ins.activate(true);

        ins.stopTiming(String.format("Random BubbleSort %d Times", numTimes));
        
    }

    private static void testInstrumentationOverhead(){;
        ins.startTiming("Run start/stop 10,000 times");
        for (int i = 0; i < 10000; i++) {
            ins.startTiming("Spam");
            ins.stopTiming("Spam");
        }
        ins.stopTiming("Run start/stop 10,000 times");
    }

    private static void testPopulateArray(){
        int[] sizes = new int[] {1000,2000,4000, 8000, 16000};
        for (int arrSize : sizes){
        String s = String.format("populateArray(%d) 10,000 times", arrSize);
        ins.startTiming(s);
        for (int i = 0; i < 10000; i++) {
            int arr[] = Test.populateArray(arrSize);
        }
        ins.stopTiming(s);
        }
        
        
    }
    
    public static void test(Instrumentation instrumentation){
        ins = instrumentation;
        BubbleSort.ins = instrumentation;
        QuickSort.ins = instrumentation;
        ins.startTiming("main");
        int n = 50; int numTimes = 1000;
        Test.testQuickSort(n, numTimes);
        Test.testBubbleSort(n, numTimes);
        //Test.testInstrumentationOverhead();
        //Test.testPopulateArray();
        ins.stopTiming("main");
        
    }
}