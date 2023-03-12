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

void QuickSort(std::vector<int> &a, int low, int high)
{
    if ((high - low) > 1)
    {
        int left_pointer = low - 1;
        int right_pointer = high + 1;

        // ensure bounds are
        ++left_pointer;
        --right_pointer;

        std::cout << "-----NEXT LOOP-----" << "\n";

        int pivot_index = floor((high + low) / 2); // get the middle
        int pivot_value = a.at(pivot_index);
        std::cout << pivot_value << "\n";

        // while left and right are within bounds
        while (left_pointer < right_pointer)
        {
            std::cout << "-----ITERATION-----" << "\n";
            PrintArray(a);
            std::cout << left_pointer << " " << a.at(left_pointer) << "\n";
            std::cout << right_pointer << " " << a.at(right_pointer)<< "\n";
            
            //getchar();
            if (a.at(left_pointer) >= pivot_value 
                && a.at(right_pointer) <= pivot_value)
                {
                    std::cout << "swap" << "\n";
                    Swap(a.at(left_pointer), a.at(right_pointer));
                    ++left_pointer;
                    --right_pointer;
                    continue;
                }

            if (a.at(left_pointer) <= pivot_value)
            {
                if (left_pointer < pivot_index)
                {
                    std::cout << "left smaller, advance" << "\n";
                    ++left_pointer;
                }
                
            }

            if (a.at(right_pointer) >= pivot_value)
            {
                if (right_pointer > pivot_index)
                {
                    std::cout << "right larger, advance" << "\n";
                    --right_pointer;
                }
            }
        }

        // Call quick sort on the lower and higher sub-arrays
        QuickSort(a, low, pivot_index);
        QuickSort(a, pivot_index + 1, high);
    }
}

int main()
{
    std::vector<int> data = {1000, 44, 2, 10, 9, 10, 18, 3, 20, 2000, 34, 1999, 3482, 23};
    std::cout << "data before sorting: "
              << "\n";
    PrintArray(data);

    QuickSort(data, 0, data.size() - 1);

    std::cout << "data after sorting: "
              << "\n";
    PrintArray(data);

    return 0;
}