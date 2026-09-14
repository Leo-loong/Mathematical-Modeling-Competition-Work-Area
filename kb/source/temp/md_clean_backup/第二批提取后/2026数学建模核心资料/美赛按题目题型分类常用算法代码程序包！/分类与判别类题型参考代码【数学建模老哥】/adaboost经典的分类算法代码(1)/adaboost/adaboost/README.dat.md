**************************************************************************
* Matlab source codes for the Boosting of the J-DLDA learner(B-JDLDA) 	*
* Author: Lu Juwei  									*
* Edited by Tejaswini G                                                 *
*      Bell Canada Multimedia Lab, Dept. of ECE, U. of Toronto          *
* Released in September 2007								*
**************************************************************************

The matlab functions implement the method presented in the paper regarding boosting of the strong J-DLDA learner[01593701.pdf]
J. Lu, K.N. Plataniotis, A.N. Venetsanopoulos, S.Z. Li, Ensemble-based Discriminant Learning with Boosting for Face Recognition,
IEEE Transactions on Neural Networks, Vol. 17, No. 1, pp. 166-178, January 2006

[desciption of files]:

R_JD_LDA_BstTrnM2V1ar.m : Main function to call. Implements the AdaBoost with JD-LDA

F_Random: Function to generate random numbers / data

F_PartTrainValid:  Partition a database into two sets: training set and validation set based on the sample distribution produced during AdaBoosting process.

F_JD_LDA_PLossVa: Function to 1. classify the elements of the training set using the individual learner, 2. compute pseudo loss.

F_AssignLabelM2V2a: Function to assign labels to test inputs using the AdaBoost learner

F_GetWgtBTW: Program to update the weighting matrix used to compute the between class scatter matrix for the individual LDAs, based on classification results
of the previous Boosting iteration

F_RandPartV4: Program to initially partition the training data into training and validation set, at iteration 1.

F_wJD_LDAV2: Program to implement weighted Juwei's D-LDA (wJD-LDA), which uses weighted between-class scatter matrix, the weights (mA) are from the
sample distribution.

array.m: Program to find the number of distinct elements in an array, and the number of times each distinct element occurs

[usage]:
Call the function R_JD_LDA_BstTrnM2V1ar() with the required parameters.

[Restrictions:]
In all documents and papers that report on research that uses the matlab codes, the researcher(s) must reference the following paper:
J. Lu, K.N. Plataniotis, A.N. Venetsanopoulos, S.Z. Li, Ensemble-based Discriminant Learning with Boosting for Face Recognition,
IEEE Transactions on Neural Networks, Vol. 17, No. 1, pp. 166-178, January 2006

Any comments and questions can be sent to juwei@dsp.utoronto.ca, tejas@comm.utoronto.ca.
