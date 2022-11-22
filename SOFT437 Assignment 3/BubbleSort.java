class BubbleSort {
    static Instrumentation ins = null;
    public static void sort(int arr[])
    {   
        ins.startTiming("bubbleSort()");
        int n = arr.length;
        for (int i = 0; i < n - 1; i++){

            for (int j = 0; j < n - i - 1; j++)
                if (arr[j] > arr[j + 1]) {
                    // swap arr[j+1] and arr[j]
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }

        }
        ins.stopTiming("bubbleSort()");

    }
 
}
