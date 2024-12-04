function rotate(nums, k) {
    k = k % nums.length;
    reverse(nums, 0, nums.length);
    reverse(nums, 0, k);
    reverse(nums, k, nums.length);
    return nums;
}

function reverse(nums, start, end) {
    while (start < end) {
        let temp = nums[start];
        nums[start] = nums[end];
        nums[end] = temp;
        start++;
        end++;
    }
}

console.log(rotate([1, 2, 3, 4, 5], 2));
console.log(rotate([1, 2, 3], 4)); 
