function [Z, Xcluster, Ycluster, A, cluster] = isodata(X, Y, k, L, I, ON, OC, OS, NO, min)
 
% ON:一个聚类中最少样本 
% OC:两聚类中心之间的最小距离.
% OS:一个聚类域中样本距离分布的标准差.
% k:期望得到的聚类数.
% L:一次迭代运算中可以合并的聚类中心的最多对数.
% I:允许迭代的次数.

s=size(X);
s=s(2);
cluster=zeros(1,s);  
iter=0;
final=0;
vuelve3=0;
A=1;     
primeravez=1;   


Z= inicializa_centros(X, Y, A);

 
while final==0,    
	 
    if primeravez==0,
		if vuelve3==0,
            [Ltemp, Itemp, ktemp, ONtemp, OCtemp, OStemp]=parametros(L, I, k, ON, OC, OS, iter);
        end;
    end;
	
	
    primeravez=0;
	vuelve3=1;
	for i=1:s,
        cluster(i)=cercano(X(i), Y(i), Z, A);
	end;
	

	[Z, A, cluster]=eliminar(A, cluster, Z, X, Y, ON);
    
   
	Z=recalcula(cluster, X, Y, A, Z);
    
	
    if (iter==I),
        final=1;
        next=0;
	else
        next=decide78(iter, k, A);
    end;


	
	if next==1,
        next=2;
        hubo_division=0;
        A2=A;
  	    divide=0;
       
        [Di, D, STM]= dispersion(X, Y, Z, cluster, A);
	
      
		i=0;                        
		while (hubo_division==0) & (i < A),                                          
		    i=i+1;                                                                                      
		    index=find(cluster==i);   
		    sindex=size(index);                                                                         
		    sindex=sindex(2);                                                                           
		    if  (STM(i)>OS) & (  ((Di(i,1)>D(1)) & (Di(i,2)>D(2)) & (sindex>(2*(ON+1)))) | (A<=(k/2)) ), 
		        hubo_division=1;                                                                        
		        next=1;                                                                                 
		        [Z, cluster]=dividir(STM, A, cluster, Z, i, (A+1), X, Y);              
		        A=A+1;                                    
		        iter=iter+1;                                                                            
		   end;                                                                                         
		end;                                                                                            

    end;

    
	
	if  next==2,
        
        [orden, Dij]= distancia_centros(A, Z, OC, L);  
        
        if  orden(1) > 0,
            [cluster, Z, A]=union(A, orden, cluster, Z, Dij);
           
            Z=recalcula(cluster, X, Y, A, Z);
        end;
	end;
	
	
	if next==2
        [iter,final,vuelve3]= termina_o_itera(iter, I, NO);
    end;
    

end;    
 

for j=1:s
    temp=0;
    P=[X(j) Y(j)];
    for i=1:A,
        if distancia(P,Z(i,:)) > min,
            temp=temp+1;
        end;
    end;
    if  temp==A,
        cluster(j)=0;
    end;
end;




Xcluster=0;
Ycluster=0;
for m=1:k
    inedx=0;
    index=find(cluster==m);
    s2=size(index);
    s2=s2(2);
    for n=1:s2
        Xcluster(1,n,m)= X(index(n));
        Ycluster(1,n,m)= Y(index(n));
    end;
end;





function [m] = cercano(x, y, Z, k)
    dtemp=0;
    d=0;
    for j=1:k
        P=[x y];
        d=distancia(Z(j,:), P); 
        if j<2,
            m=j;    
            dtemp=d;
        elseif d < dtemp,
            m=j;    
            dtemp=d; 
        end;
    end;    
    


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Zout1] = recalcula(cluster, X, Y, k, Z) 
	s=size(X);
	s=s(2);
	valor=zeros(1,k);
	Zout=zeros(k,2);
	for m=1:k
        index=find(cluster==m);
        if isempty(index)==0
            sindex=size(index);
            sindex=sindex(2);  
            Zout1(m,1)=(sum(X(index))) / sindex;
            Zout1(m,2)=(sum(Y(index))) / sindex;        
        else
            Zout1(m,:)=Z(m,:);
        end;
	end;
    


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Ditemp, Dtemp, STMAX] = dispersion(X, Y, Z, cluster, A)
    Ditemp=zeros(A,2);
    Dtemp=zeros(1,2);
    ST=zeros(A,2);
    STMAX=zeros(1,A);
    for i=1:A,
        suma=[0 0];
        index=find(cluster==i);
        sindex=size(index);
        for j=index,
            P=[X(j), Y(j)];
            d=distancia(Z(i,:), P  );
            suma(1)=suma(1) + (d * X(j));   
            suma(2)=suma(2) + (d * Y(j));   
        end;
      
        Ditemp(i,:)=suma / sindex(2);
       
        Dtemp(1,:)=Dtemp(1,:) + (Ditemp(i,:) * sindex(2)); 
       
        ST(i,1)=std(X(index));
        ST(i,2)=std(Y(index));
      
        STMAX(i)=max(ST(i,:));
    end;
   
    Dtemp(1,:)=Dtemp(1,:) / A;


 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Ztemp, Atemp, clustertemp]=eliminar(A, cluster, Z, X, Y, ON)
	 
	desplazamiento=zeros(1,A);   
	for i=1:A,                  
        cont=find(cluster==i);   
        scont=size(cont);
        
        if scont(2) < ON
            desplazamiento(i)=-1;
            if  i < A,
                for j=(i+1):A
                    desplazamiento(j)=desplazamiento(j)+1;
                end;
            end;    
        end;
	end;
	 
    [Ztemp, Atemp, clustertemp]=reduce(desplazamiento, A, cluster, Z);
	 
	 
    if isempty(Ztemp)==1,   
        Atemp=1;
        Ztemp(1,1)=median(X);
        Ztemp(1,2)=median(Y);
    end;
	vacio=find(clustertemp==0);
	if  isempty(vacio)==0
        for i=vacio,
            clustertemp(i)=cercano(X(i), Y(i), Ztemp, Atemp);
        end;
	end;
 

 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [clustertemp, Ztemp, Atemp]=union(A, orden, cluster, Z, Dij)
    clustertemp=cluster;
    sorden=size(orden);
    unidos=0;
    uindex=0;
    sunidos=size(unidos);
    marca=zeros(1,A);
    imarca=0;
    for i=1:sorden(2),
        yaunido=0;
        temp=[0 0];
       
        [fcnum(1),fcnum(2)]=find(Dij==orden(i));  
        for j=1:2,
            if isempty( find(unidos==fcnum(j)) )==0,
                yaunido=1;
            else
                temp(j)=fcnum(j);
            end;
        end;
        
        if yaunido==0
            for h=1:2;   
                unindex=uindex+1;
                unidos(unindex)=temp(h);
            end
            marca(fcnum(2))=-1;
            selec=find(clustertemp==fcnum(2));   
            clustertemp(selec)=fcnum(1);          
        end;
    end;
    
    adicion=0;   
    for i=1:A
        if  marca(i) >= 0,
            marca(i)=marca(i)+adicion;
        else
            adicion=adicion+1;
        end;
    end;
   
    [Ztemp, Atemp]=reduce(marca, A, clustertemp, Z);


 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Ztemp, Atemp, clustertemp]=reduce(desplazamiento, A, cluster, Z)
    Atemp=A;
    clustertemp=cluster;
    Ztemp=find(Atemp==999999);
    
    for i=1:A
        if  (desplazamiento(i) < 0),
            selec=find(cluster==i);
            if isempty(selec)==0
                clustertemp(selec)=0;
            end;
            Atemp=Atemp-1;
        else
            Ztemp( (i-desplazamiento(i)), :)= Z(i,:);
            selec=find(clustertemp==i);
            clustertemp(selec)=clustertemp(selec)-desplazamiento(i);
        end;
    end;


 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [orden, Dij]= distancia_centros(A, Z, OC, L)
    Dij=zeros((A-1),A);
    
    for i=1:(A-1),
        for j=(1+i):A,
            Dij(i,j)=distancia(Z(i,:), Z(j,:));
        end;
    end;
    
    
    index= find( (Dij>0) & (Dij<OC) )';
    if (isempty(index))==0,
        orden=sort(Dij(index));
        sorden=size(orden);
        if sorden(2)>L
            orden=orden(1,1:L);
        end;
    else
        orden=0;
    end;

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  分裂算法  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Ztemp, clustertemp]=dividir(ST, A, cluster, Z, ncentro, Atemp, X, Y)
    clustertemp=cluster;
    Ztemp=Z;
    k2=0.5;          % 0 < k2 < 1
    Yi=ST(ncentro) * k2;
    Ztemp(Atemp,:)=Ztemp(ncentro,:);          
    m=find( Ztemp(ncentro,:)==max(Ztemp(ncentro,:)) );     
    Ztemp(ncentro,m)=Ztemp(ncentro,m)+Yi;  % Z+=Z(ncentro)
    Ztemp(Atemp,m)=Ztemp(Atemp,m)-Yi;      % Z-=Z(Atemp)
    %  (Z+ o Z-),
    % 
    % Z+.
    dividendo= find(clustertemp==ncentro);
    for i=(dividendo),
        P=[X(i), Y(i)];
        if  (distancia( P, Ztemp(ncentro,:) )) >= (distancia(P, Ztemp(Atemp,:))),  %d(Z+) >= d(Z-)
            clustertemp(i)=Atemp;
        end;
    end;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  计算两中心距离
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [dist]= distancia(Z1, Z2)
    dist=sqrt( ((Z1(1)-Z2(1))^2) + ((Z1(2)-Z2(2))^2) );% Distancia entre dos puntos.
    
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Z]=inicializa_centros(X, Y, k)
     
    dx= (max(X))-(min(X));
    dy= (max(Y))-(min(Y));
    dzx= dx/(k+1);     
    dzy= dy/(k+1);     
    for i=1:k,
        Z(i,1)=min(X)+(dzx*i);
        Z(i,2)=min(Y)+(dzy*i);
    end;
    
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Ltemp, Itemp, ktemp, ONtemp, OCtemp, OStemp]=parametros(L, I, k, ON, OC, OS, iter)
    Ltemp=L; Itemp=I; ktemp=k; ONtemp=ON; OCtemp=OC; OStemp=OS;
    comienza=0;
    while comienza==0,
        preg=find(comienza==9); 
        fprintf('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n');
        fprintf('Iteracion actual: %d \n',iter);
        fprintf('L=%d, I=%d, k=%d, ON=%d, OC=%d, OS=%d \n',L,I,k,ON,OC,OS);
        fprintf('Que parametro deseas modificar? \n(1: L / 2: I / 3: k / 4: ON / 5: OC / 6: OS / 7: Ninguno) \n');
        while isempty(preg)==1,
            preg=input('Eleccion:');
        end;
        if preg==7
            comienza=1;
        else
            valor=find(comienza==9);% Da resultado vacio.
            while isempty(valor)==1,
                valor=input('Valor:');
            end;
            if preg==1,
                Ltemp=valor;
                elseif preg==2,
                    Itemp=valor;
                    elseif preg==3,
                        Ktemp=valor;
                        elseif preg==4,
                            ONtemp=valor;
                            elseif preg==5,
                                OCtemp=valor;
                                elseif preg==6,
                                    OStemp=valor;
            end;
        end;
    end;

    
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [itertemp,FINtemp,vuelve3temp]= termina_o_itera(iter, I, NO)
    itertemp=iter;
    FINtemp=0;
    vuelve3temp=1;
    if itertemp==I,
        FINtemp=1;
    else
        if NO==1
            vuelve3temp=1;    
        else
            preg2=find(iter==0);  
            fprintf('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n');
            fprintf('Iteracion actual: %d \n',itertemp);
            while (isempty(preg2)==1) | ( (preg2~=2) & (preg2~=1) ),
                fprintf('Desea modificar algun parametro antes de volver iterar? (SI=1 / NO=2) \n Respuesta:');
                preg2=input('');
            end;
            if preg2==1
                vuelve3temp=0;   
            else
                vuelve3temp=1;  
            end;
        end;
        itertemp=itertemp+1;
    end;
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [nexttemp]=decide78(iter, k, A)
    nexttemp=0;
    if A <= (k/2)
        nexttemp=1;      
    end
    if ( (A>=(2*k)) | ( (iter>0) & (((iter+1)/2)>(ceil(iter/2)))) )    
        nexttemp=2;      
    end
    if nexttemp==0
        nexttemp=1;
    end;