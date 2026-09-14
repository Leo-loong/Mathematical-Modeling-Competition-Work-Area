function list=F_Random(M)
% Get random data among 1:M

% -- Different random number will be generaged, even if matlab is
% -- re-started up.
rand('state',sum(100*clock));

% -- if using the following function setting, same random number will 
% -- be generated every time call.
%rand('state',0);

updlist = [1:M];
list = zeros(1, M);
i = 0;
while ~isempty(updlist)
   s = 0;
   N = size(updlist, 2);
   while s==0,
      s = fix(rem(rand*10e4, N))+1;
   end
   i=i+1;
   list(i)=updlist(s);
   updlist(s) = [];
end   