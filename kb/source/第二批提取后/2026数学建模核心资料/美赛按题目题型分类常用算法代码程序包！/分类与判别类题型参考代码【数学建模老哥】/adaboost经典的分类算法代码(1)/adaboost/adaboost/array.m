function [d nos]=array(input)
%program to find the number of distinct elements in an array, and the
%distinct elements. Also finds the number of times each distinct element
%occurs
% Syntax: [d nos]=array(input)
% Inputs
% input: vector (typically the vector with class labels)
% Outputs:
% d: no. of distinct elements in vector
% nos: a matrix, where the first column is the element of the input vector
% and the second column is the times of occurence
% Written by Tejaswini, 2007


i=1;
d=1; % no. of elements
flag=1;
s=sort(input);
j=1;
while (i<=length(s)-1)

    if (s(i)~=s(i+1))
        d=d+1;
        nos(j,1)=s(i);
        nos(j,2)=flag;
        flag=0;
        j=j+1;
    end
    i=i+1;
    flag=flag+1;
    
    
end
nos(j,1)=s(end);
nos(j,2)=flag;




%%

