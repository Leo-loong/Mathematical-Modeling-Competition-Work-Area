function [done] = maxGenTerm(ops,bPop,endPop)
currentGen = ops(1);
maxGen   = ops(2);
done      = currentGen >= maxGen;
