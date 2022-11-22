class QuickSort{
    static Instrumentation ins = null;
    static void swap(int[] arr, int i, int j)
    {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    static int partition(int[] arr, int low, int high)
    {
        //ins.startTiming(String.format("partition(%d, %d)", low, high));
        int pivot = arr[high];
        int i = (low - 1);
        for (int j = low; j <= high - 1; j++) {
            if (arr[j] < pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        //ins.stopTiming(String.format("partition(%d, %d)", low, high));
        return (i + 1);
    }
    static void quickSort(int[] arr, int low, int high)
    {
        //ins.startTiming(String.format("quickSort(%d, %d)", low, high));
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
        //ins.stopTiming(String.format("quickSort(%d, %d)", low, high));
    }
    static void printArray(int[] arr, int size)
    {
        for (int i = 0; i < size; i++)
            System.out.print(arr[i] + " ");
  
        System.out.println();
    }
    static void sort(int[] arr){
        ins.startTiming("quickSort()");
        int n = arr.length;
        quickSort(arr, 0, n - 1);
        ins.stopTiming("quickSort()");
    }
}