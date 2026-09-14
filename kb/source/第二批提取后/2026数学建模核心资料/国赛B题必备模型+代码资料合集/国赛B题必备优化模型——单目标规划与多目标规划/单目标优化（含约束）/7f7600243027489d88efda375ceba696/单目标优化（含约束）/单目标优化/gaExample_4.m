%% Basic GA parameters
gaDat.Objfun='objfun_example4';
% lb=[0,17,0.2,0,10,13];
% ub=[15,50,2,70,15,20];
lb=[0,17,2,50,20,30];
ub=[150,50,10,150,100,150];
gaDat.FieldD=[lb; ub];
% Execute GA
gaDat=ga(gaDat);
% Result are in
gaDat.xmin
gaDat.fxmin