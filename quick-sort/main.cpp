/// Summary: This program will take a vector of integer values
/// and use the quick sort algorithm to sort them.
#include <vector>
#include <iostream>
#include <bits/stdc++.h>
#include <iterator>
#include <math.h>

void PrintArray(std::vector<int> &a)
{
    for (int i : a)
    {
        std::cout << i << " ";
    }
    std::cout << "\n";
}

void Swap(int &p1, int &p2)
{
    int temp = p1;
    p1 = p2;
    p2 = temp;
}

void QuickSort(std::vector<int>& a, int low, int high) {
    if (low < high) {
        int pivot = a.at((low + high) / 2); // Get the middle point of the array
        // capture the complete bounds of each subarray
        int left_pointer = low - 1;
        int right_pointer = high + 1;
        while (true) {
            // Ensure left_pointer is incremented, and j is decremented at least once
            do {
                left_pointer++;
            } while (a.at(left_pointer) < pivot); // stop incrementing when left_pointer is == or > pivot value
            do {
                right_pointer--;
            } while (a.at(right_pointer) > pivot); // stop decrementing when right_pointer is == or < pivot value
            if (left_pointer >= right_pointer) {
                break;
            }
            // swap the lower and higher values in the array positions located at the left and right pointers
            Swap(a.at(left_pointer), a.at(right_pointer));
        }
        // recursively call quicksort on the two newly created subarrays, using right_pointer here mandates a + 1 on the
        // higher array call. This is due to the fact that the pivot itself can change position.
        // from low (bottom of the array) -> right pointer (lower side)
        QuickSort(a, low, right_pointer);
        // from right_pointer + 1 -> high
        QuickSort(a, right_pointer + 1, high);
    }
}

int main()
{
    std::vector<int> data = {-8, 1000, 44, 2, 10, 9, 10, 18, 3, 20, 521, 6, 5, 10, 8, 2000, 34, 1999, 3482, 23};
    std::cout << "data before sorting: "
              << "\n";
    PrintArray(data);

    QuickSort(data, 0, data.size() - 1);

    std::cout << "data after sorting: "
              << "\n";
    PrintArray(data);

    return 0;
}