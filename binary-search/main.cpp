/// Summary
/// this program will demonstrate a simple binary search.
/// taking a dynamic array (vector), use a binary search to find if a specific value is in the dataset and if so
/// return its index
#include <iostream>
#include <vector>
#include <cmath>
#include <string>

int BinarySearch(std::vector<int> *a, int value)
{
    int l = 0;
    int r = a->size() - 1;
    int mid_point;
    
    // each loop, redefine l, r, and mid_point depending on iterations results until value is found
    while (l <= r)
    {
        mid_point = std::floor((l + r) / 2);
        if (a->at(mid_point) < value)
        {
            l = mid_point + 1;
        }

        if (a->at(mid_point) > value)
        {
            r = mid_point - 1;
        }

        if (a->at(mid_point) == value)
        {
            return mid_point;
        }
    }

    // if the value is not found, return -1
    return -1;
}

int main()
{
    // A binary search will only work on an array that is sorted
    std::vector<int> ages = {0, 2, 3, 4, 5, 10, 16, 28, 32, 47, 55, 100, 115};
    std::string input;
    int target_value;
    
    std::cout << "What value would you like to search for? ";
    std::cin >> input;

    try 
    {
        target_value = std::stoi(input);
    }
    catch(std::exception)
    {
        std::cout << "Please enter a valid integer. Exiting program." << "\n";
        return -1;
    }    

    int index = BinarySearch(&ages, target_value);

    // ensures the value exists in the dataset
    if (index >= 0)
    {
        std::cout << "the value " << std::to_string(target_value) 
        << ", is located at index: " << std::to_string(index) << "\n";
    }
    else
    {
        std::cout << "the value " << std::to_string(target_value) 
        << " is not inside of the dataset." << "\n";
    }

    return 0;
}