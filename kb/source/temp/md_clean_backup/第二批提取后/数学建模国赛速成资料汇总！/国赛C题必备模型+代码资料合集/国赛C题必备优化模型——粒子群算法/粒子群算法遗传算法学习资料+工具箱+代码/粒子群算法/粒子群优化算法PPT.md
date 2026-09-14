<!-- 第 1 页 -->
## 群智能理论及粒子群优化算法
群智能理论及粒子群优化算法
李宁

<!-- 第 2 页 -->

<!-- 第 3 页 -->

<!-- 第 4 页 -->
## Swarm Intelligence
Swarm Intelligence
Swarm Intelligence (SI)的概念最早由Beni、Hackwood和在分子自动机系统中提出。分子自动机中的主体在一维或二维网格空间中与相邻个体相互作用，从而实现自组织。1999年，Bonabeau、Dorigo和Theraulaz 在他们的著作《Swarm Intelligence: From Natural to Artificial Systems中对群智能进行了详细的论述和分析，给出了群智能的一种不严格定义：任何一种由昆虫群体或其它动物社会行为机制而激发设计出的算法或分布式解决问题的策略均属于群智能。

<!-- 第 5 页 -->
## Swarm Intelligence(续)
Swarm Intelligence(续)
Swarm可被描述为一些相互作用相邻个体的集合体，蜂群、蚁群、鸟群都是Swarm的典型例子。鱼聚集成群可以有效地逃避捕食者，因为任何一只鱼发现异常都可带动整个鱼群逃避。蚂蚁成群则有利于寻找食物，因为任一只蚂蚁发现食物都可带领蚁群来共同搬运和进食。一只蜜蜂或蚂蚁的行为能力非常有限，它几乎不可能独立存在于自然世界中，而多个蜜蜂或蚂蚁形成的Swarm则具有非常强的生存能力，且这种能力不是通过多个个体之间能力简单叠加所获得的。社会性动物群体所拥有的这种特性能帮助个体很好地适应环境，个体所能获得的信息远比它通过自身感觉器官所取得的多，其根本原因在于个体之间存在着信息交互能力。

<!-- 第 6 页 -->
## Swarm Intelligence(续)
Swarm Intelligence(续)
信息的交互过程不仅仅在群体内传播了信息，而且群内个体还能处理信息，并根据所获得的信息（包括环境信息和附近其它个体的信息）改变自身的一些行为模式和规范，这样就使得群体涌现出一些单个个体所不具备的能力和特性，尤其是对环境的适应能力。这种对环境变化所具有适应的能力可以被认为是一种智能（关于适应性与智能之间的关系存在着一些争议，Fogel认为智能就是具备适应的能力），也就是说动物个体通过聚集成群而涌现出了智能。因此，Bonabeau 将SI的定义进一步推广为：无智能或简单智能的主体通过任何形式的聚集协同而表现出智能行为的特性。这里我们关心的不是个体之间的竞争，而是它们之间的协同。

<!-- 第 7 页 -->
## Swarm Intelligence(续)
Swarm Intelligence(续)
James Kennedy和Russell C.Eberhart在2001年出版了《Swarm Intelligence》，是群智能发展的一个重要历程碑，因为此时已有一些群智能理论和方法得到了应用。他们不反对Bonabeau关于SI定义，赞同其定义的基本精神，但反对定义中使用“主体”一词。其理由是“主体”所带有自治性和特殊性是许多Swarm的个体所不具备和拥有的，这将大大限制Swarm的定义范围。他们认为暂时无法给出合适的定义，赞同由Mark Millonas（1994）提出的构建一个SI系统所应满足的五条基本原则：

<!-- 第 8 页 -->
## Swarm Intelligence(续)
Swarm Intelligence(续)
[1]   Proximity Principle: 群内个体具有能执行简单的时间或空间上的评估和计算的能力。
[2]   Quality Principle: 群内个体能对环境（包括群内其它个体）的关键性因素的变化做出响应。
[3]   Principle of Diverse Response: 群内不同个体对环境中的某一变化所表现出的响应行为具有多样性。
[4]   Stability Principle: 不是每次环境的变化都会导致整个群体的行为模式的改变。
[5]   Adaptability Principle: 环境所发生的变化中，若出现群体值得付出代价的改变机遇，群体必须能够改变其行为模式。

<!-- 第 9 页 -->
## Swarm Intelligence(续)
Swarm Intelligence(续)
《Swarm Intelligence》最重要的观点是：Mind is social，也就是认为人的智能是源于社会性的相互作用，文化和认知是人类社会性不可分割的重要部分，这一观点成为了群智能发展的基石。群智能已成为有别于传统人工智能中连接主义和符号主义的一种新的关于智能的描述方法。
群智能的思路，为在没有集中控制且不提供全局模型的前提下寻找复杂的分布式问题求解方案提供了基础。在计算智能领域已取得成功的两种基于SI的优化算法是蚁群算法和粒子群算法。

<!-- 第 10 页 -->
## Swarm Intelligence(续)
Swarm Intelligence(续)
目前，已有的基于SI的优化算法都是源于对动物社会通过协作解决问题行为的模拟，它主要强调对社会系统中个体之间相互协同作用的模拟。这一点与EC不同，EC是对生物演化中适者生存的模拟。与EC一样的是，SI的目的并不是为了忠实地模拟自然现象，而是利用他们的某些特点去解决实际问题。另一个与EC的相同点是,基于SI的优化算法也是概率搜索算法。

<!-- 第 11 页 -->
## Swarm Intelligence(续)
Swarm Intelligence(续)
目前，已有的群智能理论和应用研究证明群智能方法是一种能够有效解决大多数优化问题的新方法，更重要是,群智能潜在的并行性和分布式特点为处理大量的以数据库形式存在的数据提供了技术保证。无论是从理论研究还是应用研究的角度分析,群智能理论及应用研究都是具有重要学术意义和现实价值的。

<!-- 第 12 页 -->
## Swarm Intelligence(续)
Swarm Intelligence(续)
由于SI的理论依据是源于对生物群落社会性的模拟，因此其相关数学分析还比较薄弱，这就导致了现有研究还存在一些问题。首先，群智能算法的数学理论基础相对薄弱，缺乏具备普遍意义的理论性分析，算法中涉及的各种参数设置一直没有确切的理论依据，通常都是按照经验型方法确定，对具体问题和应用环境的依赖性比较大。其次，同其它的自适应问题处理方法一样，群智能也不具备绝对的可信性，当处理突发事件时,系统的反应可能是不可测的,这在一定程度上增加了其应用风险。另外,群智能与其它各种先进技术(如:神经网络、模糊逻辑、禁忌搜索和支持向量机等) 的融合还不足。

<!-- 第 13 页 -->
## 蚁群算法
蚁群算法
蚁群算法（Ant Colony Optimization, ACO）由Colorni，Dorigo和Maniezzo在1991年提出，它是通过模拟自然界蚂蚁社会的寻找食物的方式而得出的一种仿生优化算法。自然界种蚁群寻找食物时会派出一些蚂蚁分头在四周游荡，如果一只蚂蚁找到食物，它就返回巢中通知同伴并沿途留下“信息素”（pheromone） 作为蚁群前往食物所在地的标记。 信息素会逐渐挥发，如果两只蚂蚁同时找到同一食物，又采取不同路线回到巢中，那么比较绕弯的一条路上信息素的气味会比较淡，蚁群将倾向于沿另一条更近的路线前往食物所在地。

<!-- 第 14 页 -->
## 蚁群算法(续)
蚁群算法(续)
ACO算法设计虚拟的“蚂蚁”，让它们摸索不同路线，并留下会随时间逐渐消失的虚拟“信息素”。根据“信息素较浓的路线更近”的原则，即可选择出最佳路线。
目前，ACO算法已被广泛应用于组合优化问题中，在图着色问题、车间流问题、车辆调度问题、机器人路径规划问题、路由算法设计等领域均取得了良好的效果。也有研究者尝试将ACO算法应用于连续问题的优化中。由于ACO算法具有广泛实用价值，成为了群智能领域第一个取得成功的实例，曾一度成为群智能的代名词，相应理论研究及改进算法近年来层出不穷。

<!-- 第 15 页 -->
## 蚁群算法(续)
蚁群算法(续)

<!-- 第 16 页 -->
## 其它群智能优化算法
其它群智能优化算法
目前，还有一些不成熟的群智能优化算法，国内值得关注的有以下几种。
2003年李晓磊、邵之江等提出的鱼群算法，它利用自上而下的寻优模式模仿自然界鱼群觅食行为，主要利用鱼的觅食、聚群和追尾行为，构造个体底层行为；通过鱼群中各个体的局部寻优，达到全局最优值在群体中凸现出来的目的。在基本运算中引入鱼群的生存机制、竞争机制以及鱼群的协调机制，提高算法的有效效率。

<!-- 第 17 页 -->
## 其它群智能优化算法（续）
其它群智能优化算法（续）
张玲等则提出了一种“松散的脑袋”群智能模型，采用特殊的随机人工神经网络构建了一种群智能数学模型。每个神经元被看成一个主体，主体之间的通讯连接看成各神经元之间的连接，但连接是随机而不是固定的，即用一个随机连接的神经网络来描述一个群体，这种神经网络来描述一个群体。显然这种神经网络具有群体的智能。
基于群智能的优化算法设计必须遵守简单有效的原则，对于自然现象过于复杂的模拟往往会导致算法不具有推广性和实用价值，许多群智能算法不成功的原因就在于此。

<!-- 第 18 页 -->
## 优化问题简介
优化问题简介

<!-- 第 19 页 -->

<!-- 第 20 页 -->

<!-- 第 21 页 -->

<!-- 第 22 页 -->

<!-- 第 23 页 -->

<!-- 第 24 页 -->

<!-- 第 25 页 -->

<!-- 第 26 页 -->
## PSO算法简介
粒子群算法(particle swarm optimization，PSO)由Kennedy和Eberhart在1995年提出，该算法模拟鸟集群飞行觅食的行为，鸟之间通过集体的协作使群体达到最优目的，是一种基于Swarm Intelligence的优化方法。同遗传算法类似，也是一种基于群体叠代的，但并没有遗传算法用的交叉以及变异，而是粒子在解空间追随最优的粒子进行搜索。PSO的优势在于简单容易实现同时又有深刻的智能背景，既适合科学研究，又特别适合工程应用，并且没有许多参数需要调整。
PSO算法简介

<!-- 第 27 页 -->
James Kennedy received the Ph.D. degree from theUniversity of North Carolina, Chapel Hill, in 1992.He is with the U.S. Department of Labor, Washington,DC. He is a Social Psychologist who has been working with the particle swarm algorithm since 1994. He has published dozens of articles and chapters on particle swarms and related topics, in computer science and social science journals and proceedings. He is a coauthor of Swarm Intelligence (San Mateo, CA: Morgan Kaufmann, 2001), with R.C. Eberhart and Y. Shi, now in its third printing.

<!-- 第 28 页 -->
Russell C. Eberhart (M’88–SM’89–F’01) received the Ph.D. degree in electrical engineering from Kansas State University, Manhattan.He is the Chair and Professor of Electrical and Computer Engineering, Purdue School of Engineering and Technology, Indiana University–Purdue University Indianapolis (IUPUI),Indianapolis, IN. He is coeditor of Neural Network PC Tools(1990),coauthor of Computational Intelligence PC Tools (1996), coauthor of Swarm Intelligence(2001), Computational Intelligence: Concepts to Implementations(2004). He has published over 120 technical papers.Dr. Eberhart was awarded the IEEE Third Millenium Medal. In 2002, he became a Fellow of the American Institute for Medical and Biological Engineering.

<!-- 第 29 页 -->
## 近年PSO方面文献的数量
近年PSO方面文献的数量

<!-- 第 30 页 -->
## PSO产生背景之一：复杂适应系统
PSO产生背景之一：复杂适应系统
CAS理论的最基本的思想可以概述如下：
我们把系统中的成员称为具有适应性的主体(Adaptive Agent)，简称为主体。所谓具有适应性，就是指它能够与环境以及其它主体进行交流，在这种交流的过程中“学习”或“积累经验”，并且根据学到的经验改变自身的结构和行为方式。整个系统的演变或进化，包括新层次的产生，分化和多样性的出现，新的、聚合而成的、更大的主体的出现等等，都是在这个基础上出现的。

<!-- 第 31 页 -->
## 复杂适应系统（CAS）续
复杂适应系统（CAS）续
CAS的四个基本特点：
首先，主体(Adaptive Agent)是主动的、活的实体；
其次，个体与环境(包括个体之间)的相互影响，相互作用，是系统演变和进化的主要动力；
再次，这种方法不象许多其他的方法那样，把宏观和微观截然分开，而是把它们有机地联系起来；
最后，这种建模方法还引进了随机因素的作用，使它具有更强的描述和表达能力。

<!-- 第 32 页 -->
## PSO产生背景之二:人工生命
PSO产生背景之二:人工生命
人工生命“是来研究具有某些生命基本特征的人工系统。人工生命包括两方面的内容：
① 研究如何利用计算技术研究生物现象；
② 研究如何利用生物技术研究计算问题(Nature Computation)。
我们现在关注的是第二部分的内容。现在已经有很多源于生物现象的计算技巧，例如, 人工神经网络是简化的大脑模型. 遗传算法是模拟基因进化过程的。现在我们讨论另一种生物系统：社会系统，更确切地说，是由简单个体组成的群落与环境以及个体之间的互动行为，也可称做"群智能"。

<!-- 第 33 页 -->
## 基本PSO算法
基本PSO算法
粒子群优化算法源于1987年Reynolds对鸟群社会系统boids的仿真研究，boids是一个CAS。在boids中，一群鸟在空中飞行，每个鸟遵守以下三条规则：
1）避免与相邻的鸟发生碰撞冲突；
2）尽量与自己周围的鸟在速度上保持协调和一致；
3）尽量试图向自己所认为的群体中靠近。
仅通过使用这三条规则，boids系统就出现非常逼真的群体聚集行为，鸟成群地在空中飞行，当遇到障碍时它们会分开绕行而过，随后又会重新形成群体。

<!-- 第 34 页 -->
## 基本PSO算法（续）
基本PSO算法（续）
Reynolds仅仅将其作为CAS的一个实例作仿真研究，而并未将它用于优化计算中 。
Kennedy和Eberhart在中加入了一个特定点，定义为食物，鸟根据周围鸟的觅食行为来寻找食物。他们的初衷是希望通过这种模型来模拟鸟群寻找食源的现象，然而实验结果却揭示这个仿真模型中蕴涵着很强的优化能力，尤其是在多维空间寻优中。

<!-- 第 35 页 -->
## 基本PSO算法(续)
基本PSO算法(续)
PSO中，每个优化问题的解都是搜索空间中的一只鸟。称之为“粒子(Particle)”。所有的粒子都有一个由被优化的函数决定的适应值，每个粒子还有一个速度决定他们飞翔的方向和距离。然后粒子们就追随当前的最优粒子在解空间中搜索.
PSO 初始化为一群随机粒子。然后通过叠代找到最优解。在每一次叠代中，粒子通过跟踪两个"极值"来更新自己。第一个就是粒子本身所找到的最优解。这个解叫做个体极值pBest. 另一个极值是整个种群目前找到的最优解。这个极值是全局极值gBest。另外,也可以不用整个种群而只是用其中一部分的邻居。

<!-- 第 36 页 -->
## 基本PSO算法(续)
基本PSO算法(续)
PSO算法数学表示如下：
设搜索空间为D维，总粒子数为n。第i个粒子位置表示为向量Xi=( xi1, xi2,…, xiD )；第i个粒子 “飞行”历史中的过去最优位置（即该位置对应解最优）为Pi=( pi1,pi2,…,piD )，其中第g个粒子的过去最优位置Pg为所有Pi ( i=1, …,n)中的最优；第i个粒子的位置变化率（速度）为向量Vi=(vi1, vi2,…, viD)。每个粒子的位置按如下公式进行变化（“飞行”）：

<!-- 第 37 页 -->
## 基本PSO算法(续)
基本PSO算法(续)
（1）
（2）
其中，C1,C2为正常数，称为加速因子；rand(  )为[0，1]之间的随机数；w称惯性因子，w较大适于对解空间进行大范围探查(exploration)，w较小适于进行小范围开挖(exploitation)。第d（1≤d≤D）维的位置变化范围为[-XMAXd , XMAXd]，速度变化范围为[-VMAXd , VMAXd]，迭代中若位置和速度超过边界范围则取边界值。

<!-- 第 38 页 -->
## 基本PSO算法(续)
基本PSO算法(续)
粒子群初始位置和速度随机产生，然后按公式(1)(2)进行迭代，直至找到满意的解。目前，常用的粒子群算法将全体粒子群(Global)分成若干个有部分粒子重叠的相邻子群，每个粒子根据子群(Local)内历史最优Pl调整位置，即公式(2)中Pgd换为Pld。

<!-- 第 39 页 -->
## PSO与EC的异同
PSO与EC的异同
首先，PSO和EC所模拟的自然随机系统不一样。EC是模拟生物系统进化过程，其最基本单位是基因，它在生物体的每一代之间传播；而PSO模拟的是社会系统的变化，其最基本单位是“敏因”（Meme），这一词由Dawkin在《The Selfish Gene》一书中提出，它是指思想文化传播中的基本单位，个体在社会中会根据环境来改变自身的思想，Meme的传播途径是在个体与个体之间，在实际人类社会中它还可以在人脑与书本之间、人脑与计算机、计算机与计算机之间传播。

<!-- 第 40 页 -->
## PSO与EC的异同（续）
PSO与EC的异同（续）
其次，EC中强调“适者生存”，不好的个体在竞争中被淘汰；PSO强调“协同合作”，不好的个体通过学习向好的方向转变，不好的个体被保留还可以增强群体的多样性。EC中最好的个体通过产生更多的后代来传播自己的基因，而PSO中的最佳个体通过吸引其它个体向它靠近来传播自己的敏因。

<!-- 第 41 页 -->
## PSO与EC的异同（续）
PSO与EC的异同（续）
再次，EC中的上一代到下一代转移概率只与上一代的状态相关，而与历史无关，它的个体只包含当前信息，其群体的信息变化过程是一个Markov链过程；而PSO中的个体除了有着位置和速度外，还有着过去的历史信息（pBest、gBest），也就是具有记忆能力，上一代到下一代转移概率不仅与上一代的状态相关，而且与过去的历史相关，如果仅从群体的位置及速度信息来看，群体的信息变化过程不是一个Markov链过程。

<!-- 第 42 页 -->
## PSO与EC的异同（续）
PSO与EC的异同（续）
最后，EC的迭代由选择、变异和交叉重组操作组成，而PSO的迭代中的操作是“飞行”。在某种程度上看，PSO的操作中隐含了选择、变异和交叉重组操作，gBest和pBest的更新可以类似一种弱选择；而粒子位置更新则类似于3个父代：Xi、gBest和pBest的之间重组，其中还包含了变异的成分。PSO中所隐含的变异是有偏好的，而并非通常的完全随机变异，这与最近对实际生物系统变异行为的新研究成果相符。

<!-- 第 43 页 -->
## PSO与EC的异同（续）
PSO与EC的异同（续）
EC和PSO所分别模拟的两个伟大的自然随机系统：Evolution和Mind之间存在着显著的差异，尽管它们都是基于群体的，都是由其中的随机成分带来创新，但其本质是不同的，因此不能将PSO简单地归类于EC中。

<!-- 第 44 页 -->
## Particle Swarm研究热点
Particle Swarm研究热点
IEEE TRANSACTION ON EVOLUTIONARY COMPUTION于2004年出版了第3卷：SPECIAL ISSUE ON PSO。Russell C.Eberhart, Yuhui Shi在卷首语中指出了当前PSO研究的几个主要方向及热点：
1。算法分析；
2。粒子群拓扑结构；
3。参数选择与优化；
4。与其他演化计算的融合；
5。应用。

<!-- 第 45 页 -->
## 粒子运动轨迹的分析
粒子运动轨迹的分析
为了便于分析和表达，首先将问题空间简化为一维的，分别用    、 表示式（2.5）中的             和               ，仅研究粒子群中的某一个粒子i的运动过程，并暂时先假设pBest、gBest在粒子i运动过程中不变，于是可得粒子i运动的状态方程组（3.1）和（3.2），这将是本节分析和讨论的对象。
（3.1）
（3.2）

<!-- 第 46 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
将式（3.1）和（3.2）递推可得到：
（3.4）
（3.6）
由上可知，粒子的速度和位置变化过程均是二阶差分方程，本节将对它们做分析。

<!-- 第 47 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
对（3.4）做Z变换，由Routh判据，二阶线性系统稳定的充分必要条件是特征方程各项系数均为正值，于是可得到差分方程（3.4）稳定的条件为（取某一个条件等号时系统系统等幅周期振荡，速度不趋于无穷大，此处可认为临界稳定）
（3.14）

<!-- 第 48 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
当满足（3.14）中条件均取严格不等号时，由Z变换的终值定理可得：
（3.15）
也就是在不考虑随机量且pBest、gBest位置不变的假设下，当满足（3.14）中严格不等于条件时，单个粒子的速度将趋向0。

<!-- 第 49 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
同理，对（3.6）做Z变换，由Routh判据，可得到差分方程（3.6）稳定的条件为：
（3.25）

<!-- 第 50 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
当满足条件（3.25），由Z变换的终值定理可得：
（3.26）
这说明，在不考虑随机量且pBest、gBest位置不变的假设下，当满足式（3.25）中条件时，单个粒子的位置将趋向

<!-- 第 51 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
本文以上分析方法所得到的结果（3.25）式与文献[9]所得的最终结果（2.8）式不一致，图3.1给出两种不同约束条件所得到的范围，细斜线左上方的灰色区域为本文所得到的单个粒子可收敛区域，而文献[9]中（2.8）式所对应的仅是粗实线上所有的点，显然本文约束条件（3.25）式所得的范围比文献[9]的范围大很多，并包含了文献[9]的范围，而文献[9]约束条件（2.8）式的表达要比式（3.25）复杂些。

<!-- 第 52 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
图3.1 两种不同约束条件得到的范围

<!-- 第 53 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
pBest、gBest分别代表粒子的“自身经验”和“社会经验”，粒子通过它们和群体实现协同合作，因此其变化是不可忽视的。这个系统的输入的变化过程是未知的，而且与粒子本身的运动过程还存在着弱反馈关系，那么式（3.26）所给出的粒子最终位置是否仅是一种理想状态的结果呢？
当pBest、gBest发生变化时，粒子的位置是否能跟踪上是不肯定的。

<!-- 第 54 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
pBest和gBest的变化过程符合如下式（3.27）（3.28）的规律：
（3.27）
（3.28）
都是递减的，而且当优化问题的值空间有限且存在全局最优值时候，它们存在下界。

<!-- 第 55 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
若f(x)不是2.2.3节（NFL定理）中所说的欺骗函数和随机函数，而是第三类函数，而且f(pi(t)),f(Pg(t))的变化pi(t),pg(t)与的变化之间存在着类似梯度信息的规律。那么当搜索时间无限时， f(pi(t)),f(Pg(t))和pi(t),pg(t)在粒子群搜索的初期过程中会变化比较剧烈，随后pi(t),pg(t)将逐步逼近某个值，而f(pi(t)), f(Pg(t))也将趋于稳定或停滞，因此系统后期的输入pi(t),pg(t)可以被看作是一个阶跃函数，在不考虑随机成分的情况下系统的输出将能够跟踪上

<!-- 第 56 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
粒子群在多数实际寻优过程中无论是找到了最优解或是陷入某个局部最优解，还是算法停滞，整个过程中的gBest变化将会逐步减小，最终趋于停止，pBest将逐步趋向gBest。因此当搜索时间无限时，所有粒子的位置将逐步靠近并停止于                                              处。

<!-- 第 57 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
在随机启发式优化算法中随机量的作用是非常重要的，正是随机量所带来的不确定性给整个粒子群带来了多样性和创新。去掉随机量后，单个粒子的运动过程成为了一个二阶线性系统，使得分析变得比较简单，但这个便于分析的假设条件使得以上对粒子运动行为的分析具有很大的局限性。下面将进一步讨论随机量对粒子运动行为的影响。

<!-- 第 58 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
为便于分析，式（3.22）中初始值取                   ，并对也取Z变换可得到：
（3.30）
不考虑            与      之间存在的弱反馈关系，式（3.30）所对应的系统如图3.8所示。

<!-- 第 59 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）

<!-- 第 60 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
由仿真实例可以看出，当PSO参数不满足式（3.25）的条件时，粒子的运动轨迹也可能收敛到                                   ；而当PSO参数满足式（3.25）的条件时，粒子的运动轨迹却不一定能保证收敛到一个固定位置。显然，随机性的存在使得粒子运动轨迹是否收敛到一个固定点并不完全遵照式（3.25）所给出的规律。

<!-- 第 61 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
实验研究发现，粒子群中粒子运动轨迹收敛到固定点的概率与参数选择存在着密切关系。当参数不满足式（3.25）所给出条件时，绝大多数粒子的运动轨迹都是不收敛到一个固定点的，除了一些特例，例如粒子群中某个粒子找到全局最优解，且当前速度为0，则该粒子运动轨迹肯定收敛。当参数满足式（3.25）所给出条件时，参数越接近条件的边界粒子运动轨迹收敛的几率越小，反之越大。一般而言，w越大不收敛的概率越大，c1、c2越大不收敛的概率越大，其中w的影响更大些。

<!-- 第 62 页 -->
## 粒子运动轨迹的分析（续）
另外，粒子运动轨迹不收敛到固定点时，其振荡幅值与参数选择也存在着密切关系。当参数不满足式（3.25）时，振荡幅值很大，甚至发散；满足式（3.25）时，振荡幅值要小许多，且振荡的幅值在一定范围内，在某种意义上粒子处于广义稳定状态，这样的状态对粒子群的搜索是有益的。其中w越大振荡幅值越大，c1、c2越大振荡幅值越大，其中的影响更大些。
粒子运动轨迹的分析（续）

<!-- 第 63 页 -->
## 粒子运动轨迹的分析（续）
粒子群中的粒子运动轨迹处于发散振荡状态显然是对算法收敛无益的，而处于幅值有限的振荡状态对算法是有非常重要的作用。粒子运动轨迹振荡幅值很大时可以看作是算法的开拓能力强，而当粒子轨迹振荡幅值较小时则是开掘能力强。是否能通过PSO参数的选择来调整粒子运动轨迹的振荡幅值呢？
粒子运动轨迹的分析（续）

<!-- 第 64 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）
若PSO参数一直满足条件（3.25）,则粒子运动轨迹振荡的幅值是有限的。这个二阶振荡环节的阻尼系数为：
（3.32）
二阶振荡系统的阻尼系数越小，系统振荡的幅值越大。式（3.32）表明，尽管存在随机量，但通过选择和调节PSO参数还是可以对粒子的振荡幅值实现控制的。

<!-- 第 65 页 -->
## 粒子运动轨迹的分析（续）
粒子运动轨迹的分析（续）

<!-- 第 66 页 -->
## 粒子运动轨迹的分析（续）
以上讨论说明，条件（3.25）还是非常有意义的。针对优化问题的特点，通过式（3.25）和（3.32）可以选择合理的PSO参数，调整粒子运动轨迹的振荡幅值使得粒子群的开拓能力和开掘能力均能得到兼顾，从而可提高算法的成功率。另外，还可以在运算过程中动态地改变参数，使得粒子的运动的振荡幅度由大到小，在搜索的前期粒子更多地体现开拓能力，而后期粒子更多地发挥开掘能力。因此，式（3.25）和（3.32）是有重要价值的，有助于实际应用PSO算法参数择和使用的理论公式和条件。
粒子运动轨迹的分析（续）

<!-- 第 67 页 -->
## PSO算法收敛性分析
PSO算法收敛性分析
随机算法收敛的标准
对于优化问题           ，有随机优化算法D，第k次迭代的结果XK，下一次迭代的结果为                   ，其中  是算法D这次迭代中曾经搜索过的解。
条件H1：                            ，且若         ，则有                              。
条件H1可保证随机算法的正确性，其目的是希望能保证优化算法的解的适应度值是非递增的。

<!-- 第 68 页 -->
## PSO算法收敛性分析(续)
PSO算法收敛性分析(续)
条件H2：对                              ，有：                    。
其中         为算法第k次迭代的结果在集合B上的概率测度。算法满足条件H2意味着，A中任意满足          的子集B，算法D连续无穷次未搜索到A中点的几率为0。因为             ，那么满足条件的算法连续无穷次搜索不到近似全局最优点的概率为0。
条件H3：对             ，                                 为紧集，且             ，         和           ，有：

<!-- 第 69 页 -->
## PSO算法收敛性分析(续)
PSO算法收敛性分析(续)
定理3.1（算法全局收敛）：假设f是可测度的，可行解空间A是Rn上可测度的子集，算法D满足条件(H1)(H2)，                                                                           是算法D产生数列，则有：
定理3.2（算法局部收敛）：假设f是可测度的，可行解空间A是Rn上可测度的子集，算法满足条件(H1)(H3)，         是算法D产生数列，则有：

<!-- 第 70 页 -->
## PSO算法收敛性分析(续)
PSO算法收敛性分析(续)
定义3.1（粒子状态和粒子状态空间） 粒子的位置x，速度v以及历史最佳位置p（pBest）构成粒子的状态O=(x,v,p)，简称粒子，其中x,p在可行解集A中，且x,p∈A,在速度范围[vmin,vmax]内。所有可能的粒子状态的集合构成粒子状态空间
简称粒子空间。
定义3.2（粒子群状态和粒子群状态空间）粒子群中所有N个粒子的状态的集合称为粒子群状态，简称粒子群                          。所有可能的粒子群状态的集合构成粒子群状态空间                                                             。

<!-- 第 71 页 -->
## PSO算法收敛性分析(续)
PSO算法收敛性分析(续)
定义3.3（粒子群等价） 对于               ，记                         ，其中      表示事件A的示性函数，         表示粒子群状态中包含粒子状态的数目。若有两个粒子群             ，对于          ，若有                        ，则称S1和S2等价，记作～  。
定理3.3 “～”是S上的等价关系。

<!-- 第 72 页 -->
## PSO算法收敛性分析(续)
PSO算法收敛性分析(续)
定义3.4（粒子群状态等价类）由等价关系“~”在S上诱导的粒子群状态等价类记作L=~/S，简称粒子群等价类。
定理3.4   等价关系“~”在S上诱导的等价类划分L=~/S的个数为：

<!-- 第 73 页 -->
## PSO算法收敛性分析(续)
PSO算法收敛性分析(续)
定理3.13 在数字计算机实现的标准PSO算法中，粒子群状态序列              是有限齐次Markov链。
定理3.14 在数字计算机实现的标准PSO算法中，粒子群等价类状态序列            是有限齐次Markov链。

<!-- 第 74 页 -->
## PSO算法收敛性分析(续)
PSO算法收敛性分析(续)
定义3.19（最优粒子状态集） 设优化问题           的全局最优解为    ，定义粒子最优状态集                                           。
定义3.20（最优粒子群状态集） 设优化问题         的全局最优解为     ，定义最优粒子群状态集                                       。

<!-- 第 75 页 -->
## PSO算法收敛性分析(续)
PSO算法收敛性分析(续)
定理 3.17 PSO算法中，对粒子群状态序列             而言，最优粒子群状态集合G是状态空间S上的一个闭集。
定理3.19 当          时，状态空间S中至少存在一个G之外的闭集，即

<!-- 第 76 页 -->
## PSO算法的收敛性分析（续）
PSO算法的收敛性分析（续）
S
G
B

<!-- 第 77 页 -->
## PSO算法收敛性分析(续)
PSO算法收敛性分析(续)
定理3.20 当         时，PSO算法是无法保证全局收敛的。
定理 3.21当          时，PSO算法是无法保证局部收敛的。
尽管PSO算法是无法保证收敛的，但这并不意味着PSO算法的性能不好。本节研究结果的意义首先可用于指导算法的改进。同时，本节所提出的方法更是为PSO算法的理论分析和研究提供了一种新的思路，可在此基础上对PSO算法的进一步的理论研究。

<!-- 第 78 页 -->
## PSO理论分析的其它可能方法
PSO理论分析的其它可能方法
目前，能对PSO算法进行理论分析的有效数学手段还很少，本文了提出的两个新的分析手段，在微观上采用差分方程，在宏观上采用Markov链。除此之外，是否还存在其它的分析方法和手段呢？根据对其它随机算法讨论和分析的经验以及PSO算法的特点，下面对其它可能的分析方法和手段作简单的讨论。

<!-- 第 79 页 -->
## 随机过程中的其它方法
随机过程中的其它方法
本文采用了随机过程中的Markov链方法对PSO算法做分析。但如果独立分析粒子群的位置转换序列，它显然不是一个Markov链，是否可以采用随机过程中的其它方法直接对进行分析呢？例如，可以把粒子的运动看成一个随机变量，它的变化都有着一定的确定性，也存在着一定的不确定性，能否用熵或相对熵来描述粒子运动离散分布的不确定性的大小，从而对算法的收敛率做分析呢？

<!-- 第 80 页 -->
## 随机过程中的其它可能方法（续）
随机过程中的其它可能方法（续）
另外，就PSO算法迭代的随机过程而言，总是希望这个过程在期望值意义下越来越好，这自然应当是一个下鞅序列，因此可利用鞅收敛定理就可对算法的收敛性进行分析。同时也可以看到，要保证算法的收敛，有两个参数很重要：一个是过程进入满意解之后下一步脱离满意解的可能性；另一个是未进入满意解时下一步仍不能进入满意解的可能性。利用这种方法得到结果可能直观而且简练，也许对如何改进PSO算法会有重要指导意义。

<!-- 第 81 页 -->
## 基于混沌动力学理论
基于混沌动力学理论
一个好的PSO系统既非稳定态也非混沌态，而是一种处于两者之间临界态的自组织复杂系统。从系统工程的角度而言，PSO应该是一个连续的非线性动态系统，因此将复杂系统的研究方法，将混沌理论中的非线性动力学引入PSO的分析和改进研究应该是非常有前途的。

<!-- 第 82 页 -->
## 基于混沌动力学理论（续）
基于混沌动力学理论（续）
此类分析方法能充分体现PSO系统中粒子间的相互作用的意义和随机性的价值。但如何采用混沌动力学理论来描述粒子群系统也存在一些困难，如何定义PSO系统中的吸引子、轨道、分叉和稳定性等概念都是要解决的问题。另外，非线性系统的稳定性只能针对某个解来谈的，而不能一般地讨论系统的稳定性，而且系统的稳定性与优化算法的收敛性之间存在什么样的关系也是未知的，因此如何通过这类方法来分析算法的收敛性和性能是目前是未知的。

<!-- 第 83 页 -->
## 二维图元约束布局优化
二维图元约束布局优化
A total number of n circular dishes with uniform thickness and mass distribution will be located on a circular bearing plate with a radius R as shown in Fig. 1. Suppose ri and mi (i∈I) are the radius and mass of the i th dish, respectively.

<!-- 第 84 页 -->
The basic problem is to find the position of each dish so that all the dishes can highly concentrate to the center of the bearing plate while the following conditions exist.  (a) No overlap exists between any two dishes. (b) No dish protrudes out of the bearing plate. (c) The static equilibrium error of the whole system should not exceed a permissible value [δj].

<!-- 第 85 页 -->
Suppose that the Cartesian coordinate system coincides with the symmetric axis of the bearing plate and Xi=(xi, yi) is the centroid of the ith dish. Then the mathematical model of the above problem can be described as the following.
Find
(1)
S.t.  ① No overlap exists between any two dishes：
(2)
② No part of any dish protrudes out  of the plate:
(3)
③ The static equilibrium error：
(4)

<!-- 第 86 页 -->
## Particle Swarm Optimization with Mutation Operator
Particle Swarm Optimization with Mutation Operator
This paper introduces a mutation operator to basic PSO, something like GA. If the historic optimal position Pl keeps continuously unchanged or has changed extremely a little, in other word, the particle swarm aggregates heavily, we will keep Pl and re-random several dimension of particles according to certain probability to improve global searching ability without decreasing the convergent speed and search accuracy.

<!-- 第 87 页 -->
## The pseudocode of PSO with mutation operator
The pseudocode of PSO with mutation operator
While k<MaxIterations & ActualError>AcceptableError
If LogjamStep>=MaxStep
If SwarmRadius<BorderRadius
Re-random the position and velocity of several data of each
particles according to mutation probability ρ;
LogjamStep=0;
Else
LogjamStep=LogjamStep+1;
End
End
Update the position and velocity according to Eq. (1) and Eq. (2)
End

<!-- 第 88 页 -->
## Test suite 1
Test suite 1
| TABLE 1 RESULTS OF LAYOUT SCHEME FOR TEST SUIT 1 |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| No | Initial layout scheme |  | Layout scheme by HCIGA |  | Layout scheme By PSO |  |
|  | r(mm) | m(g) | x(mm) | y(mm) | x(mm) | y(mm) |
| 1 | 10.0 | 100.00 | -12.883 | 17.02 | 14.367 | 16.453 |
| 2 | 11.0 | 121.00 | 8.847 | 19.773 | -18.521 | -9.560 |
| 3 | 12.0 | 144.00 | 20.662 | 0.000 | 2.113 | -19.730 |
| 4 | 11.5 | 132.00 | -8.379 | -19.43 | 19.874 | -4.340 |
| 5 | 9.5 | 90.25 | -1.743 | 0.503 | -19.271 | 11.241 |
| 6 | 8.5 | 72.25 | 12.368 | -18.989 | -3.940 | 22.157 |
| 7 | 10.5 | 110.25 | -21.639 | -1.799 | -0.946 | 2.824 |
In the test suite, the radius of the round container is R, which equals to 50mm, and the number of the round to-be-laid objects is 7. Suppose the acceptable value of the static equilibrium error, J, is [δJ=3.4 g·mm], and the other data of the to-be-laid objects and the result of the layout is shown in TABLE 1.

<!-- 第 89 页 -->
(a) Layout Pattern by HCIGA    (b) Layout Pattern by PSO
| TABLE 2  COMPARISON OF LAYOUT SCHEMES FOR TEST SUIT 1 |  |  |  |
|---|---|---|---|
| Algorithm | GA Ref [11] | HCIGA | PSO |
| Radius of the out warp circle (mm) | 32.837 | 32.662 | 31.843 |
| Static equilibrium error (g.mm) | 0.102 | 0.029 | 0.0022 |
| Interference (mm) | 0 | 0 | 0 |
| Computation time (s) | 1735 | 1002 | 1874 |
| Ps: The computation time is converted into the time of the computer with 166M main frequency, by using PSO, when the calculated radius of the out wrap circle is 32.66, the computation time is 760 seconds. |  |  |  |

<!-- 第 90 页 -->
Repeat the test suit by PSO for 40 times, and the results are shown as TABLE 3, that is, every time the result all satisfies the restrict conditions, and the mean radius of the out wrap circle is 32.49mm.
| TABLE 3  RESULTS OF 40 TIMES COMPUTATION FOR TEST SUIT 1 |  |  |  |  |
|---|---|---|---|---|
| Radius of the out warp circle (mm) | ≤32.3 | ( 32.3, 32.5] | (32.5, 32.7] | (32.7,32.9] |
| Times | 10 | 16 | 5 | 2 |
| Radius of the out warp circle (mm) | (32.9, 33.1] | (33.1,33.3] | >33.3 |  |
| Times | 2 | 2 | 3 |  |

<!-- 第 91 页 -->
## Test Suit 3
Test Suit 3
In order to prove the availability of PSO further, the known most optimal solution in the test suit of [8] is quoted. In the big round container, of which the radius is R=125mm, five to-be-laid objects are laid out. The data of the to-be-laid objects and the result of the layout are shown in TABLE 6. (In  [8], the population size of GA, M, is 60, while in this paper, the number of the PSO particles, M, is 60, and the population size of neighborhood is 2, and c1=c2=1.49, and w=0.729, and the maximum number of iteration is 200.)

<!-- 第 92 页 -->
| Table 6 RESULTS OF LAYOUT SCHEME FOR TEST SUIT 3 |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| No | r (mm) | m (kg) | Optimization (Known quantity) |  | SAGA |  | PSO |  |
|  |  |  | x(mm) | y(mm) | x(mm) | y(mm) | x(mm) | y(mm) |
| 1 | 20.71 | 20.71 | 0.00 | 0.000 | -0.586 | -1.058 | 0.000 | 0.000 |
| 2 | 50.00 | 50.00 | 70.71 | 0.000 | 65.979 | 26.179 | 0.000 | 70.71 |
| 3 | 50.00 | 50.00 | 0.00 | 70.71 | -26.25 | 68.061 | 70.71 | -0.000 |
| 4 | 50.00 | 50.00 | 0.00 | -70.71 | 27.891 | -66.89 | 0.000 | -70.71 |
| 5 | 50.00 | 50.00 | -70.71 | 0.000 | -66.69 | -26.89 | -70.71 | 0.000 |

<!-- 第 93 页 -->
(a) Optimization        (b) Layout Pattern      (c) Layout Pattern
Layout Pattern          by SAGA             by PSO
| Table 7 COMPARISON OF LAYOUT SCHEMES FOR TEST SUIT 3 |  |  |  |
|---|---|---|---|
| Algorithm | SAGA | GA | PSO |
| Radius of the out warp circle (mm) | 123.200 | 121.434 | 120.711 |
| Static equilibrium error (g.mm) | 1.265 | 0.0010 | 0.002712 |
| Interference (mm) | 0 | 0 | 0 |
| Computation  time(s) | 648 | 306 | 287 |

<!-- 第 94 页 -->
Layout Pattern of the global optima and usual local optima of show in Fig 2,  if λ1 =1, λ2 =1, λ3 =0.01.

<!-- 第 95 页 -->
To measure the effectiveness and viability of PSO with mutation operator, results are compared with basic local PSO and Multi Start PSO. The max iteration is 1000，size of population is 60, MaxStep=10,ρ=20% and . Results are presented in Table 7, 50 runs for each algorithm.

<!-- 第 96 页 -->
## 带时间窗车辆路径问题
带时间窗车辆路径问题
车辆路径问题(Vehicle Routing Problem，VRP)由Dantzig和Ramser于1959年首次提出的，它是指对一系列发货点(或收货点)，组成适当的行车路径，使车辆有序地通过它们，在满足一定约束条件的情况下，达到一定的目标(诸如路程最短、费用最小，耗费时间尽量少等)，属于完全NP问题，在运筹、计算机、物流、管理等学科均有重要意义。

<!-- 第 97 页 -->
## 带时间窗车辆路径问题（续）
带时间窗车辆路径问题（续）
带时间窗的车辆路径问题(Vehicle Routing Problem With Time Windows, VRPTW)是在VRP问题上加了客户要求访问的时间窗口。由于在现实生活中许多问题都可以归结为VRPTW问题来处理(如邮政投递、火车及公共汽车的调度等)，其处理的好坏将直接影响到企业的服务质量,所以对它的研究越来越受到人们的重视。先后出现了一般启发式算法和神经网络、遗传算法、禁忌搜索和模拟退火等智能化启发式算法，也取得了一些较好的效果。

<!-- 第 98 页 -->
## 带时间窗车辆路径问题（续）
带时间窗车辆路径问题（续）
时间窗车辆路径问题一般描述为：有一个中心仓库，拥有车K辆，容量分别为qk (k=1,..,K)；现有L个发货点运输任务需要完成，以1,…,L表示。第i个发货点的货运量为gi (i=1,…,L)，( max(g)i≤max(qi) )，完成发货点i任务需要的时间(装贷或卸货)表示为Ti，且任务i且必须在时间窗口[ETi , LTi]完成，其中ETi为任务i的允许最早开始时间，LTi为任务i的允许最迟开始时间。如果车辆到达发货点i的时间早于ETi，则车辆需在i处等待；如果车辆到达时间晚于LTi，任务i将被延迟进行。求满足货运要求的运行费用最少的车辆行驶线路。

<!-- 第 99 页 -->
时间窗车辆路径问题的数学描述：

<!-- 第 100 页 -->
## 带时间窗车辆路径问题（续）
带时间窗车辆路径问题（续）
这个模型通用性很强，经过参数的不同设定，可以将其转换为其他组合优化问题的数学模型。若(1)中ETi=0, LTi→∞，则VRPTW模型就变成了普通的VRP模型；若仅有一个车辆被利用，则该问题就变成了TSP问题；若去掉约束(2)，则变成了m－TSPTW问题。

<!-- 第 101 页 -->
## 带时间窗车辆路径问题（续）
带时间窗车辆路径问题（续）
如何找到一个合适的表达方法，使粒子与解对应，是实现算法的关键问题之一。构造一个2L维的空间对应有L个发货点任务的VRP问题，每个发货点任务对应两维：完成该任务车辆的编号k，该任务在k车行驶路径中的次序r。为表达和计算方便，将每个粒子对应的2L维向量X分成两个L维向量：Xv (表示各任务对应的车辆)和Xr(表示各任务在对应的车辆路径中的执行次序)。

<!-- 第 102 页 -->
例如，设VRP问题中发货点任务数为7，车辆数为3，若某粒子的位置向量X为：
发货点任务号:    1    2    3    4    5    6    7
Xv  ：   1    2    2    2    2    3    3
Xr  ：   1    4    3    1    2    2    1
则该粒子对应解路径为：
车1：0  1  0
车2：0  4 5  3 2 0
车3：0  7 6 0
粒子速度向量V与之对应表示为Vv和Vr。

<!-- 第 103 页 -->
该表示方法的最大优点是使每个发货点都得到车辆的配送服务，并限制每个发货点的需求仅能由某一车辆来完成，使解的可行化过程计算大大减少。虽然该表示方法的维数较高，但由于PSO算法在多维寻优问题有着非常好的特性，维数的增加并未增加计算的复杂性，这一点在实验结果中可以看到。

<!-- 第 104 页 -->
VRP问题为整数规划问题，因此在算法实现过程中要作相应修改。具体实现步骤如下：
Step1：初始化粒子群。
1.1 粒子群划分成若干个两两相互重叠的相邻子群；
1.2 每个粒子位置向量Xv的每一维随机取1～K（车辆数）之间的整数，Xr的每一维随机取1～L(发货点任务数)之间的实数；
1.3 每个速度向量Vv的每一维随机取-(K-1)～(K-1)（车辆数）之间的整数，Vr的每一维随机取-(L-1)～(L-1)之间的实数；
1.4 用评价函数Eval评价所有粒子；
1.5 将初始评价值作为个体历史最优解Pi，并寻找各子群内的最优解Pl和总群体内最优解Pg。

<!-- 第 105 页 -->
Step2：重复执行以下步骤，直到满足终止条件或达到最大迭代次数。
2.1 对每一个粒子，按式(1)计算Ｖv、Ｖr；按照式(2)计算Xv、Xr，其中Xv向上取整；当Ｖ、X超过其范围时按边界取值；
2.2 用评价函数Eval评价所有粒子；
2.3 若某个粒子的当前评价值优于其历史最优评价值，则记当前评价值为该历史最优评价值，同时将当前位置向量记为该粒子历史最优位置Pi;
2.4 寻找当前各相邻子群内最优和总群体内最优解，若优于历史最优解则更新Pl 、Pg。对于子群内有多个体同为最优值的情况，则随机取其中一个为子群内当前最优解。

<!-- 第 106 页 -->
其中，评价函数Eval完成以下任务:
1、根据公式计算该粒子所代表路径方案的行驶成本Z，在计算中发货点任务的执行次序要根据对应Xr值的大小顺序，由小到大执行。
2、将Xr按执行顺序进行重新整数序规范。例如，某粒子迭代一次后结果如下：
Xv  ：   1     2     2       2       2      3      3
Xr  ：   5    3.2   6.2   1.2    2.5   0.5    4.2
则评价后重新规范的Xr是：1     3      4       1      2       1      2

<!-- 第 107 页 -->
实验１：采用了无时间窗VRP的例子，问题为一个有7个发货点任务的车辆路径问题，各任务点的坐标及货运量见下表：
| 表1 各发货点坐标及货运量 |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| 序 号 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 坐 标 | (18,54) | (22,60) | (58,69) | (71,71) | (83,46) | (91,38) | (24,42) | (18,40) |
| 货运量 (gi) |  | 0.89 | 0.14 | 0.28 | 0.33 | 0.21 | 0.41 | 0.57 |
| 注：序号0表示中心仓库，设车辆容量皆为q=1.0，由3辆车完成所有任务。(最优路径距离为217.81) |  |  |  |  |  |  |  |  |

<!-- 第 108 页 -->
GA参数：群体规模n=40；交叉概率Pc=0.6；变异概率Pm=0.2；轮盘赌法选择子代，最大代数200。
PSO参数：粒子数n=40；分为2个子群，子群规模为22，子群间重叠的粒子数为2个（子群规模的1/10）；w=0.729；c1=c2=1.49445；最大代数200。
两种方法各运行50次，结果如下表2所示。
| 表2 实验1 GA、PSO方法结果对比 |  |  |  |  |
|---|---|---|---|---|
| 方法 | 达到最优路径次数 | 未达最优路径次数 | 达到最优路径平均代数 | 达到最优路径的平均时间(s) |
| GA | 32 | 18 | 53.9 | 32.3 |
| PSO | 50 | 0 | 28.36 | 3.04 |

<!-- 第 109 页 -->
实验2，采用VRPTW的例子，该问题有8项货物运输任务，货物点位置及时间窗略。实验结果如下：
| 表6  实验2 GA、PSO方法结果对比 |  |  |  |
|---|---|---|---|
|  | 搜索成功率 | 平均行驶成本 | 平均成功搜索时间 |
| GA | 24% | 993.6 | 18.41s |
| PSO | 46% | 940.5 | 8.53s |

<!-- 第 110 页 -->
## Evolving Neural Networks
Evolving Neural Networks
Evolve neural network capable of being universal approximator, such as backpropagation or radial basis function network.
In backpropagation, most common PE transfer function is sigmoidal function:  output = 1/(1 + e - input )
PSO can also be used to indirectly evolve the structure of a network.  An added benefit is that the preprocessing of input data is made unnecessary.

<!-- 第 111 页 -->
## Evolving Neural Networks
Evolving Neural Networks
Evolve both the network weights and   the slopes of sigmoidal transfer functions of hidden and output PEs.
If transfer function now is:  output =  1/(1 + e -k*input ) then we are evolving k in addition to evolving the weights.
The method is general, and can be applied to other topologies and other transfer functions.
Flexibility is gained by allowing slopes to be positive or negative.  A change in sign for the slope is equivalent to a change in signs of all input weights.

<!-- 第 112 页 -->
## Evolving Neural Networks
Evolving Neural Networks
If evolved slope is sufficiently small, sigmoidal output can be clamped to 0.5, and hidden PE can be removed.  Weights from bias PE to each PE in next layer are increased by one-half the value of the weight from the PE being removed to the next-layer PE.  PEs are thus pruned, reducing network complexity.
If evolved slope is sufficiently high, sigmoid transfer function can be replaced by step transfer function.  This works with large negative or positive slopes.  Network computational complexity is thus reduced.

<!-- 第 113 页 -->
## Evolving Neural Networks
Evolving Neural Networks
Since slopes can evolve to large values, input normalization is generally not needed.  This simplifies applications process and shortens development time.
The PSO process is continuous, so neural network evolution is also continuous.  No sudden discontinuities exist such as those that plague other approaches.

<!-- 第 114 页 -->
## Other applications
Other applications
Scheduling (Integrated automated container terminal)
Manufacturing (Product content combination optimization)
Figure of merit for electric vehicle battery pack
Optimizing reactive power and voltage control
Medical analysis/diagnosis (Parkinson’s disease and essential tremor)
Human performance prediction (cognitive and physical)

<!-- 第 115 页 -->
Questions and Answers
Thank you!
