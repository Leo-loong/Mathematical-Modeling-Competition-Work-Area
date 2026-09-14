Logistic模型
自然界中存在着一种事物的发展规律：在其发展初期，数量或规模增加得越来越快，到了一定时期，其增长速度逐步慢下来，最终数量或规模不再增长，从而稳定在数量或规模的极限值处。
如果记 EMBED Equation.KSEE3  \* MERGEFORMAT 时刻数量为 EMBED Equation.KSEE3  \* MERGEFORMAT ，则上述发展规律可由微分方程描述：
 EMBED Equation.KSEE3  \* MERGEFORMAT   （1）
在初始条件 EMBED Equation.KSEE3  \* MERGEFORMAT 和参数 EMBED Equation.KSEE3  \* MERGEFORMAT 已知的条件下， EMBED Equation.KSEE3  \* MERGEFORMAT 被唯一确定。易得其解为
 EMBED Equation.KSEE3  \* MERGEFORMAT    （2）
给出由 EMBED Equation.KSEE3  \* MERGEFORMAT 对观测数据 EMBED Equation.KSEE3  \* MERGEFORMAT   EMBED Equation.KSEE3  \* MERGEFORMAT 确定参数 EMBED Equation.KSEE3  \* MERGEFORMAT 及 EMBED Equation.KSEE3  \* MERGEFORMAT 估计值的算法。该问题实质是确定估计函数：
	 EMBED Equation.KSEE3  \* MERGEFORMAT
使得函数 EMBED Equation.KSEE3  \* MERGEFORMAT 和 EMBED Equation.KSEE3  \* MERGEFORMAT 的距离最小。
交替迭代算法
交替迭代算法的基本思想是：先假设 EMBED Equation.KSEE3  \* MERGEFORMAT 已知，求出 EMBED Equation.KSEE3  \* MERGEFORMAT 的最小二乘估计值，再以 EMBED Equation.KSEE3  \* MERGEFORMAT 的估计值为已知，求出 EMBED Equation.KSEE3  \* MERGEFORMAT 的最优估计值，这样交替迭代，直至收敛到符合精度要求为止。
 EMBED Equation.KSEE3  \* MERGEFORMAT 已知时 EMBED Equation.KSEE3  \* MERGEFORMAT 的估计
整理式（2）得
 EMBED Equation.KSEE3  \* MERGEFORMAT
由于观察过程中，观察数据有偏差，不妨令该偏差为
 EMBED Equation.KSEE3  \* MERGEFORMAT
其中， EMBED Equation.KSEE3  \* MERGEFORMAT 为 EMBED Equation.KSEE3  \* MERGEFORMAT 时刻的观测值，则令
 EMBED Equation.KSEE3  \* MERGEFORMAT
根据最小二乘准则，得
 EMBED Equation.KSEE3  \* MERGEFORMAT     （3）
由式（3）可见，由于对数运算的限制，只有 EMBED Equation.KSEE3  \* MERGEFORMAT 估计才有意义。
 EMBED Equation.KSEE3  \* MERGEFORMAT 已知时 EMBED Equation.KSEE3  \* MERGEFORMAT 的估计
由式（2）可得观测值：
 EMBED Equation.KSEE3  \* MERGEFORMAT
设由 EMBED Equation.KSEE3  \* MERGEFORMAT 的估计值产生的关于 EMBED Equation.KSEE3  \* MERGEFORMAT 的误差为 EMBED Equation.KSEE3  \* MERGEFORMAT ，且 EMBED Equation.KSEE3  \* MERGEFORMAT 为独立、等方差、均值为零的随机变量。
于是在第 EMBED Equation.KSEE3  \* MERGEFORMAT 时刻有
 EMBED Equation.KSEE3  \* MERGEFORMAT
那么 EMBED Equation.KSEE3  \* MERGEFORMAT 。
整理得
 EMBED Equation.KSEE3  \* MERGEFORMAT
当 EMBED Equation.KSEE3  \* MERGEFORMAT 足够大时， EMBED Equation.KSEE3  \* MERGEFORMAT 将变得非常小，这是因为
 EMBED Equation.KSEE3  \* MERGEFORMAT
因此，当 EMBED Equation.KSEE3  \* MERGEFORMAT 足够大时，
 EMBED Equation.KSEE3  \* MERGEFORMAT 。
则关于 EMBED Equation.KSEE3  \* MERGEFORMAT 的近似最小二乘估计为
 EMBED Equation.KSEE3  \* MERGEFORMAT    （4）
由 EMBED Equation.KSEE3  \* MERGEFORMAT 已知时 EMBED Equation.KSEE3  \* MERGEFORMAT 的估计和 EMBED Equation.KSEE3  \* MERGEFORMAT 已知时 EMBED Equation.KSEE3  \* MERGEFORMAT 的估计的分析可以看到，待估计参数 EMBED Equation.KSEE3  \* MERGEFORMAT 要比每个观测值 EMBED Equation.KSEE3  \* MERGEFORMAT 大，并且观测的数据量要足够远，使得 EMBED Equation.KSEE3  \* MERGEFORMAT 充分大。换句话说，在样本观察中应该有阻滞增长的事实。
算法步骤
估计 EMBED Equation.KSEE3  \* MERGEFORMAT 的交替迭代算法的具体步骤：
取初值 EMBED Equation.KSEE3  \* MERGEFORMAT （ EMBED Equation.KSEE3  \* MERGEFORMAT 接近 EMBED Equation.KSEE3  \* MERGEFORMAT ）和精度 EMBED Equation.KSEE3  \* MERGEFORMAT ，代入式（3）求得 EMBED Equation.KSEE3  \* MERGEFORMAT 的估计值 EMBED Equation.KSEE3  \* MERGEFORMAT ，即
令 EMBED Equation.KSEE3  \* MERGEFORMAT ，得
 EMBED Equation.KSEE3  \* MERGEFORMAT
将 EMBED Equation.KSEE3  \* MERGEFORMAT 代入式（4）求得 EMBED Equation.KSEE3  \* MERGEFORMAT ，
 EMBED Equation.KSEE3  \* MERGEFORMAT
若 EMBED Equation.KSEE3  \* MERGEFORMAT ，则停止，此时有 EMBED Equation.KSEE3  \* MERGEFORMAT ， EMBED Equation.KSEE3  \* MERGEFORMAT ，否则转到步骤四。
级 EMBED Equation.KSEE3  \* MERGEFORMAT ࠀࠐࠔࠖࢼࢾࣄࣆऒऔघढत॰ॲॴॶঘচজ২৪৬৮৺ৼਆਈ੔벤볡賡뱷퇡䩟̨४ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮푪阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨콪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮퍪阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̮퉪阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Ĩᔜ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊ᰀࠀࠖࢾচৼମஐൺුດຢႀᄶᅆᆨᇘሮዲፈ፞Ꮒᑎòá팀á팀á밀ááá팀á팀á팀á팀áᘀ옍搂鈑Ğᄂᲄሂ⁤ā᐀䠁$䑗È葠Ȝ摧㟣̀Ĥ搒ĠꐔǴ⑈愀Ĥ摧㟣ᄀᲄሂ⁤ā᐀䠁$䑗È葠Ȝ摧㟣ఀ␃ሁ⁤ā᐀愁Ĥ摧㟣ᔀ੔੖੘ਗ਼੠੢મરલ઴ૂૄଐ଒ଔଖବମର୼폨꺾꺾膖꺾꺾呩꺾비®ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃牪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮흪阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨ၪ
ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮홪阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨챪	ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮핪阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ጁ୼୾஀ஂஎஐ஖஘௤௦௨௪௴௶ూౄెైొౌಘ폨꺾꺞꺾熆꺾꺾䑙꺾꺾̨繪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨뉪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨晪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᐁಘಚಜಞದನ೴೶೸೺೼೾ൊൌൎ൐൸ൺർൾ්폨꺾꺾膖꺾꺾呩꺾깄꺾ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃㕪$ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨䙪!ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨鹪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᐁ්෌෎ැිුොෞสฬฮะาิ຀ຂຄຆຒດ폨꺾꺞꺾熆꺾꺾䑙꺾̨Ꙫ.ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨덪+ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨j'ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ጁດຠຢໂໄ༐༒༔༖༠༢཮཰ིུྊྌ࿘࿚듉鳉뒇듉濉둚듉䋉̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨4ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨읪1ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Ĩᔥ騷ᘀ騷㔀脈䩃䩏䩐䩑࡜澁Ĩᔥ騷ᘀ⽨더㔀脈䩃䩏䩐䩑࡜澁Ĩሀ࿚࿜࿞࿲࿴၀၂၄၆ၾႀႂ჎აგელ훫훆껆횙视幱⭃幱̮索=ᔀ騷ᘀ⽨더㔀脈䩃䩏䩐䩑ࡕ封脈⡯̴阂੉Ĉ栕㟣栖启³࠵䎁ᭊ伀͊倀͊儀͊唀Ĉࡖ封脈⡯ᔥ騷ᘀ⽨더㔀脈䩃䩏䩐䩑࡜澁Ĩ̮jᔀ騷ᘀ⽨더㔀脈䩃䩏䩐䩑ࡕ封脈⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃:ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨7ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ခლნᄨᄪᄬᄮᄴᄶᅄᅆᅈᆔᆖᆘᆚᆦᆨᇖ헨ꊺ헨羏婯䉿娭潿̨뉪Cᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Ĩᔥ騷ᘀ騷㔀脈䩃䩏䩐䩑࡜澁Ĩ̮@ᔀ騷ᘀ⽨더㔀脈䩃䩏䩐䩑ࡕ封脈⡯̴阂੉Ĉ栕㟣栖启³࠵䎁ᭊ伀͊倀͊儀͊唀Ĉࡖ封脈⡯ᔥ騷ᘀ⽨더㔀脈䩃䩏䩐䩑࡜澁Ĩ̮jᔀ騷ᘀ⽨더㔀脈䩃䩏䩐䩑ࡕ封脈⡯ᄁᇖᇘᇚሦረሪሬሮሴሶኂኄኆኈኊኌዘዚዜዞደዲዴፀ닊쫯쫚炅쫚쫚䍘쫚Ę̂Nᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨Kᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨앪Gᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Ĩᜀፀፂፄፆፈ፜፞፠ᎬᎮᎰᎲᏀᏂᏪᏬᐸᐺᐼᐾᑌᑎ폨꺾꺞麾熆麾麮麾䑙麾®̨Ὢ\ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨﹪Vᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨칪Qᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔁᑎᑐᒜᒞᒠᒢᒨᒪᓶᓸᓺᓼᔂᔄᔚᔜ헨ꊺ헨헨澇헨䱜<ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Ĩᔥ騷ᘀ騷㔀脈䩃䩏䩐䩑࡜澁Ĩ̮魪bᔀ騷ᘀ⽨더㔀脈䩃䩏䩐䩑ࡕ封脈⡯̴阂੉Ĉ栕㟣栖启³࠵䎁ᭊ伀͊倀͊儀͊唀Ĉࡖ封脈⡯̮콪_ᔀ騷ᘀ⽨더㔀脈䩃䩏䩐䩑ࡕ封脈⡯̴阂੉Ĉ栕㟣栖启³࠵䎁ᭊ伀͊倀͊儀͊唀Ĉࡖ封脈⡯ᔥ騷ᘀ⽨더㔀脈䩃䩏䩐䩑࡜澁Ĩ̮jᔀ騷ᘀ⽨더㔀脈䩃䩏䩐䩑ࡕ封脈⡯༁ᑎᔄᔜᕲᜊᝮោᠠᠨ᡾᥊ᦠᨈ᩠᫐ᬲḚḤẘ⃄℠ⅶ∴⊊îàîîààààîËà쬀à᐀☊଀ņᄀᲄሂ⁤ā᐀䠁$䑗È葠Ȝ摧㟣̀Ĥ搒ĠꐔǴ⑈愀Ĥ摧㟣ᄀᲄሂ⁤ā᐀䠁$䑗È葠Ȝ摧㟣ᜀᔜᔞᕪᕬᕮᕰᕲᕶᕸᗄᗆᗈᗊᗜᗞᘪᘬᘮᘰᘸᘺᚆ껃黫蛛姛Ų̂왪lᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨홪iᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃衪eᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᔁᚆᚈᚊᚌᚐᚒᛞᛠᛢᛤᜈᜊᜒ᜔ᝠᝢᝤᝦᝬᝮᝰូ폨꺾꺾膖꺾깱꺾䑙꺾빱®̨륪uᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃륪rᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨륪oᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔁូើៀែោៈ៊᠖᠘᠚᠜᠞ᠠᠦᠨᠪᡶᡸ᡺᡼᡾ᢀᢂᣎ폨꺾뺞蚞빱꺞꺞麾䑙꺾뺞̨㝪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨|ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨詪xᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᜁᣎᣐᣒᣔᣞᣠ᤬᤮ᤰᤲ᥈᥊᥌ᦘᦚᦜᦞᦠᦨᦪ᧶폨꺾꺾膖꺾빱妮비깱꺾̨啪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ﭪ阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃䉪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮頻阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨剪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮索阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᐁ᧶᧸᧺᧼ᨆᨈᨊᩖᩘᩚᩜᩞ᩠ᩦᩨ᪶᪸᪺᪴ᫎ᫐᫒ᬞ폨꺾뺞蚮빱麮뺮妮비麮꺾̨坪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮﹪阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨쑪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ﵪ阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨핪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ﱪ阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᘁᬞᬠᬢᬤᬰᬲ᬴ᬶᮂᮄᮆᮈᮎᮐᯜᯞᯠᯢᯪᯬ᰸폨꺾꺞꺾熆꺾꺾䑙꺾꺾̨孪§ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮Ū阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨湪¤ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮j阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨䕪ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ｪ阂੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᐁ᰸᰺᰼᰾᱄᱆ᲒᲔᲖᲘᲸᲺᴆᴈᴊᴌᴚᴜᵨᵪ폨꺾꺾膖꺾꺾呩꺾꺾<̮ժ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨¯ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮Ѫ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨¬ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ͪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨❪ªᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ɪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ጁᵪᵬᵮᶐᶒᷞᷠᷢᷤḘḚḢḤḨḪṶṸṺṼẖẘ훫훆껆횙视捶훆䯆혶视̨籪¹ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ݪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔥ騷ᘀ騷㔀脈䩃䩏䩐䩑࡜澁Ĩᔥ騷ᘀ⽨더㔀脈䩃䩏䩐䩑࡜澁Ĩᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃쁪µᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮٪阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨콪²ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᐁẘẞẠỬỮỰỲỴỶὂὄ὆ὈὌ὎ᾚᾜᾞᾠᾨᾪῶῸ싯闯棯㯯̮୪阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨偪Ãᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮੪阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨䝪Àᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮४阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨륪¼ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ࡪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀ĨᘀῸῺῼ‐⁜⁞⁠⁢⁪⁬₸₺₼₾⃂⃄⃆⃈℔№훫훆껆횙훆臆홬峆훆䓆̮๪阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃흪Ëᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮൪阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨౪Éᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮౪阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨㕪Æᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᐁ№℘ℚ℞℠™Ⅾⅰⅲⅴⅶⅸⅺ⇆⇈⇊⇌⇜⇞∪∬훫뛆웖覞뛖훆燆활훆䓆̮ᅪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨汪×ᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ၪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨䍪Òᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ཪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨Îᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᐁ∬∮∰∲∴∶⊂⊄⊆⊈⊊⊌⊎⋚⋜⋞⋠⋰⋲⌾⍀훫뛆웖覞뛖훆燆활훆䓆̮ᑪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨蕪âᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮፪阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯̨佪Ýᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ቪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Ĩᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨㡪Úᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᐁ⍀⍂⍄⍆⍈⎔⎖⎘⎚⎬⎮⎰⎲⏾␀娀娂娄娔娖娢훫훆껆횙视훆燆婯웖䞉ᔥ騷ᘀ⽨더㔀脈䩃䩏䩐䩑࡜澁Į̃ᡪíᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯唃Ĉ̮ᙪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ騷䌀ᭊ伀͊倀͊儀͊漀Į̃뭪éᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̮ᕪ阃੉Ĉ栕㟣栖启³䩃䩏䩐䩑ࡕ嘁Ĉ⡯ᔟ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊漀Į̃jᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯̨歪æᔀ騷ᘀ⽨더䌀ᭊ伀͊倀͊儀͊唀Ĉ⡯ᐁ⊊⎮娖娤尠尮岄巊帠帨怬悂扦押旸机杄杒枠桾êÙÙ츀Ù쀀ÙÀÀÙÙ«᐀☊଀Ɇᄀᲄሂ⁤ā᐀䠁$䑗È葠Ȝ摧㟣̀Ĥ搒ĠꐔǴ⑈愀Ĥ摧㟣
ሀ⁤ā᐀䠁$摧㟣ᄀᲄሂ⁤ā᐀䠁$䑗È葠Ȝ摧㟣᐀☊଀ņᄀᲄሂ⁤ā᐀䠁$䑗È葠Ȝ摧㟣ጀ；再转到步骤二。
算法的收敛性
上述参数估计问题可概述为数学问题：由 EMBED Equation.KSEE3  \* MERGEFORMAT 对观测数据 EMBED Equation.KSEE3  \* MERGEFORMAT  ，其中 EMBED Equation.KSEE3  \* MERGEFORMAT ，求式（2）的参数 EMBED Equation.KSEE3  \* MERGEFORMAT 和 EMBED Equation.KSEE3  \* MERGEFORMAT 估计值问题。
令误差函数为
 EMBED Equation.KSEE3  \* MERGEFORMAT
显然 EMBED Equation.KSEE3  \* MERGEFORMAT 为连续可微函数，那么点集 EMBED Equation.KSEE3  \* MERGEFORMAT 为一有界闭集。该问题中第 EMBED Equation.KSEE3  \* MERGEFORMAT 步迭代后的误差损失为
 EMBED Equation.KSEE3  \* MERGEFORMAT
（5）
由叙述可知，在由 EMBED Equation.KSEE3  \* MERGEFORMAT 求 EMBED Equation.KSEE3  \* MERGEFORMAT 过程中，使函数 EMBED Equation.KSEE3  \* MERGEFORMAT 的 EMBED Equation.KSEE3  \* MERGEFORMAT 部分达到最少，当这样交替复进时，非负函数 EMBED Equation.KSEE3  \* MERGEFORMAT 的值逐步达到最小。即
 EMBED Equation.KSEE3  \* MERGEFORMAT
由点集 EMBED Equation.KSEE3  \* MERGEFORMAT 的有闭性及序列 EMBED Equation.KSEE3  \* MERGEFORMAT 的非负不增性，可知存在点 EMBED Equation.KSEE3  \* MERGEFORMAT 为序列 EMBED Equation.KSEE3  \* MERGEFORMAT 的聚点， EMBED Equation.KSEE3  \* MERGEFORMAT ，即
 EMBED Equation.KSEE3  \* MERGEFORMAT
注1：由于式（5）的 EMBED Equation.KSEE3  \* MERGEFORMAT 函数是关于自变量的非线性函数，尽管在无扰动的情况下有意义，且最优解存在，但在实际观察中，误差的存在很容易使得 EMBED Equation.KSEE3  \* MERGEFORMAT 在时间 EMBED Equation.KSEE3  \* MERGEFORMAT 足够长（即 EMBED Equation.KSEE3  \* MERGEFORMAT 非常接近 EMBED Equation.KSEE3  \* MERGEFORMAT ）时失去计算意义，为了在估算参数 EMBED Equation.KSEE3  \* MERGEFORMAT 中避免该情况，观察时间 EMBED Equation.KSEE3  \* MERGEFORMAT 值不宜太大，这往往是符合实际的。
注2：从式（4）的推导过程中可得：当 EMBED Equation.KSEE3  \* MERGEFORMAT 越接近 EMBED Equation.KSEE3  \* MERGEFORMAT ， EMBED Equation.KSEE3  \* MERGEFORMAT 估计值的误差方差越小。
算法示例
参数估计算法
根据注1、2，在应用交替迭代算法估计Logistic模型中的参数时，应注意：
因观测数据 EMBED Equation.KSEE3  \* MERGEFORMAT 含有误差，所以要按由小到大重新排序，使得 EMBED Equation.KSEE3  \* MERGEFORMAT 。
观测时间要足够长，从样本上可以看出这是一个阻滞增长过程。
初始值 EMBED Equation.KSEE3  \* MERGEFORMAT 一般取第一个观测值。
参数 EMBED Equation.KSEE3  \* MERGEFORMAT 的取值范围为 EMBED Equation.KSEE3  \* MERGEFORMAT ，这里 EMBED Equation.KSEE3  \* MERGEFORMAT ， EMBED Equation.KSEE3  \* MERGEFORMAT 。
参数计算过程中，使用的样本要满足 EMBED Equation.KSEE3  \* MERGEFORMAT 。
估计 EMBED Equation.KSEE3  \* MERGEFORMAT 时应用较靠前的观测数据，而估计 EMBED Equation.KSEE3  \* MERGEFORMAT 时用靠后的数据，靠前的数据观测值多些，但不要靠近极限值，靠后的数据数目可少些，尽量靠近系统的极限。
以下 EMBED Equation.KSEE3  \* MERGEFORMAT 替换为 EMBED Equation.KSEE3  \* MERGEFORMAT ， EMBED Equation.KSEE3  \* MERGEFORMAT 替换为 EMBED Equation.KSEE3  \* MERGEFORMAT
x=0:1:12
y=[43.65 109.86 187.21 312.67 496.58 707.65 960.25 1238.75 1560.00 1824.29 2199.00 2438.89 2737.71]
y=L/(1+a*exp(-k*x))
利用线性回归模型所得到的a和k的估计值和L=3000作为Logistic模型的拟合初值，对Logistic模型做非线性回归。
%第一步,线性回归模型得到a,k
%这里假定y=a*exp(k*x),对两边取ln(Matlab中，ln用log函数表示),有
%lny=lna+k*x
%即logy是x的线性函数，斜率为k,截距为loga
x=0:1:12 ;
y=[43.65 109.86 187.21 312.67 496.58 707.65 960.25 1238.75 1560.00 1824.29 2199.00 2438.89 2737.71] ;
line_A=polyfit(x,log(y),1);
poly2str(line_A,x)
k=line_A(1);
a=exp(line_A(2));
plot(x,y,'*',x,a*exp(k*x))
title('线性回归的参数曲线与已经点的关系')
%第二步，Logistic模型
%在Matlab下输入：edit，然后将下面两行百分号之间的内容，复制进去，保存
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function y=zhidao_liziqiangde(A,x)
%其中k=A(1),a=A(2)
k=A(1);
a=A(2);
L=3000;
y=L./(1+a*exp(-k*x));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%返回Matlab，输入
[ABC,res]=lsqcurvefit('zhidao_liziqiangde',[k,a],x,y);
kk=ABC(1)
aa=ABC(2)
y_logistic=zhidao_liziqiangde(ABC,x);
figure
plot(x,y,'*',x,y_logistic)
legend('实验数据点','Logistic模型')
