Gaussian Belief Propagation Resources

- 





  
  
    
Gaussian Belief Propagation 
Resources 


  
  
     
    Hebrew 
      University
Computer 
      Science
DANSS 
Lab


  
  
     
      Home


      Projects

Papers

People

 -->
	  Download

	
		Report

		Presentation
   

 -->
       


       


       


       


       


    
       


      Theory Papers 
      
- Gaussian belief propagation: theory and application. D. Bickson. 
      Ph.D. Thesis. Submitted to the senate of the Hebrew University of 
      Jerusalem, October 2008. Revised July 2009. arxiv 
      
- Distributed fault detection via non-parametric belief propagation. D. 
      Bickson, H. Avissar, D. Dolev, S. P. Boyd, A. Ihler and D. Baron. 
      Manuscript in preperation. arxiv 
      
- Distributed sensor selection via Gaussian belief propagation. D. 
      Bickson and D. Dolev. Manuscript in preperation. arxiv 
      
- Low density lattice decoding via non-parametric belief propagation. D. 
      Bickson, A. Ihler and D. Dolev. 47h Annual Allerton Conference on 
      Communication, Control and Computing, Allerton House, Illinois, Sept. 
      2009, to appear. arxiv 
      
- Fixing the convergence of the Gaussian belief propagation algorithm. 
      J. K. Johnson, D. Bickson and D. Dolev. In the International symposium 
      on information theory (ISIT), July 2009. arxiv 
      
- Distributed large scale network utility maximization. D. Bickson, Y. 
      Tock, A. Zymnis, S. Boyd and D. Dolev. In the International symposium 
      on information theory (ISIT), July 2009. arxiv 
      
- Gaussian belief propagation for solving systems of linear equations: 
      theory and application. O. Shental, D. Bickson, P.H. Siegel, J.K. Wolf and 
      D. Dolev. Submitted to IEEE Transactions on Information Theory, October 
      2008. arxiv 
      
- Distributed Kalman filter via Gaussian belief propagation. D. Bickson, 
      O. Shental and D. Dolev, In the 46th Annual Allerton Conference on 
      Communication, Control and Computing, Allerton House, Illinois, Sept. 
      2008. arxiv 
      
- Polynomial linear programming with Gaussian belief propagation. D. 
      Bickson, Y. Tock, O. Shental and D. Dolev, In the 46th Annual Allerton 
      Conference on Communication, Control and Computing, Allerton House, 
      Illinois, Sept. 2008. arxiv 
      
- Gaussian belief propagation solver for systems of linear equations. O. 
      Shental, D. Bickson, P. H. Siegel, J. K. Wolf, and D. Dolev, In IEEE 
      Int. Symp. on Inform. Theory (ISIT), Toronto, Canada, July 2008. pdf 
      
- Gaussian belief propagation based multiuser detection. D. Bickson, O. 
      Shental, P. H. Siegel, J. K. Wolf, and D. Dolev, In IEEE Int. Symp. on 
      Inform. Theory (ISIT), Toronto, Canada, July 2008. pdf 
      
- Linear Detection via Belief Propagation. Danny Bickson, Danny Dolev, 
      Ori Shental, Paul H. Siegel and Jack K. Wolf. In the 45th Annual 
      Allerton Conference on Communication, Control, and Computing, Allerton 
      House, Illinois, Sept. 07. pdf 
      
- A message-passing solver for linear systems, O. Shental, D. Bickson, 
      P. H. Siegel, J. K. Wolf, and D. Dolev, In Proc. Information Theory and 
      Applications (ITA) Workshop, San Diego, CA, USA, January 2008. pdf 

      


      Large-Scale Applications 


      
- A statistical approach to monitoring of soft-real time distributed 
      systems. D. Bickson, G. Gershinsky, E. Hoch and K. Shagin. In ICDCS 2009, 
      submitted for publication. Nov. 2008. arxiv 
      
- A unifying framework for rating users and data items in Peer-to-Peer 
      and social networks. Danny Bickson and Dahlia Malkhi. In Peer-to-Peer 
      Networking and Applications (PPNA) Journal, Accepted, January 2008. pdf 
      
- Peer杢o-Peer Rating. Danny Bickson, Dahlia Malkhi and Lidong Zhou. 
      In the 7th IEEE Peer-to-Peer Computing, Galway, Ireland, Sept. 
      2007. pdf 
      
- A Gaussian Belief Propagation Solver for Large Scale Support Vector 
      Machines. D. Bickson, D. Dolev and E. Yom-Tov. In the 5th European 
      Complex Systems Conference.,Sept. 2008. pdf 
      Source Code gabp.m run_gabp.m
	(synch/parallel version).
	
- Matlab source code of the GaBP algorithm (asynch/serial version) asynch_GBP.m
	
- Matlab source code of the GaBP Min-Sum algorithm by Moallemi gabpms.m run_gabpms.m
	
- Optional: assert function for Matlab versions before 7.5 assert.m
	
- Source code for Newton iteration toy example:  gabp.m newtondemogbp.m
	
- Sparse GaBP Matlab code (optimized), tested with instances of size 500,000 x 500,000 with
	4% non zeros. sparse_gabp.m run_sparse_gabp.m
	
- Source code for fixing the convergence of GaBP (using the multiuser detection problem) 
    multiuser_detection.m
	multiuser_detection_fix.m
    
- Source code for the extended low density lattice decoder. run_LDLC.m LDLC.m

	This codes needs the KDE Matlab package by A. T. Ihler, found here. After unpacking, you should addpath()
	in Matlab to the root kde directory.
    -->


      
- Gaussian belief propagation Matlab package
Written by Danny 
      Bickson. gabp-src.rar
The 
      following algorithms are implemented: 
      
        
        
          gabp.m, run_gabp.m
          Gaussian BP - parallel version
        
          asynch_GBP.m
          Gaussian BP - serial version
        
          sparse_gabp.m, run_sparse_gabp.m
          Gaussian BP - sparse version, optimized, tested on sparse 
            matrices of size 0.5M x 0.5M , with 4% non zeros
        
          gabpms.ms, run_gabpms.m
          Quadratic Min-Sum algorithm - Moallemi and Van-Roy
        
          LP/
          Linear programming using GaBP (Allerton 2008 paper) arxiv 
        
          GaBP_convergence_fix/
          Fixing the convergence of the GaBP algorithm, mulituser 
            detection example (ISIT 2009) arxiv 
        
          LDLC/
          Low density lattice decoder (LDLC) using gaussian mixtures
        
          NUM/
          Distributd large scale network utility maximization (ISIT 2009) 
            arxiv 
        
          ILP/
          Non-parametric belief propagation (NBP) implementation via Alex 
            Ihler's Matlab KDE toolbox.
        
          NBP/
          New!! Non-parametric belief propagation (NBP) 
            implementation via quantization (more efficient), including working 
            compressive sensing example and boolean least squares (multiuser 
            detection) example. This code was extensively tested in Dror Baron's 
            compressive sensing journal 
        paper

        
          SS/
          Distributed sensor selection via GaBP. Manuscript in 
            preperation. arxiv 
        
        
          NBP_decoder/
          New!! Non-parametric belief propagation (NBP) decoder for 
            low density lattice codes. Allerton 2009. arxiv 
        
          fault_detection/
          Distributed fault detection via NBP. arxiv
      

Acknowledgements 
      
- This research was partially supported by ISF (Israeli Science 
      Foundation) grant number 0397373. 
      
- LDLC/ILP code relies on Alex Ihler's Matlab KDE package found here 
      
- The LDLC algorithm was implemented with the great help of Naftali 
      Sommer, Tel Aviv University. 
      
- NBP/LDLC encoding matrices were kindly provided by Marilynn Green, 
      Nokia Siemens Networks Research Technology Platforms Dallas, TX. 
      
- The non-parametric BP implementation heavily relies on Dror Baron's compressive sensing 
      decoder 
      
- The NUM simulation and the fault detection simulation was originally 
      written by Argyris Zymnis - found here 
      
- An excellent discrete BP matlab code package by Talya Meltzer is found 
      here 
      
- The sensor selection simulation was originally written by Joshi - 
      found here 

      Are you using my code? Drop me a note! I would like to hear about 
      it! Danny DOT Bickson @ GMAIL DOT COM 


      Number of unique visitors since April 19, 2009:  
Web Counters 
      
      

      
      
      
  
    
      Original site design by Pegasus Web Design Resources, modified 
      by David 
  Rabinowitz
