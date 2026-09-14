function [h,g]=cons(x) 
     h=[ ];
     g=[2-x(1)-x(2);x(1);x(2)];