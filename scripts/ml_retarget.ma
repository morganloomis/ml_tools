//Maya ASCII 2022 scene
//Name: scene.ma
//Last modified: Fri, Dec 05, 2025 10:00:44 AM
//Codeset: 1252
requires maya "2022";
requires -nodeType "aiOptions" -nodeType "aiAOVDriver" -nodeType "aiAOVFilter" "mtoa" "5.0.0.4";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2022";
fileInfo "version" "2022";
fileInfo "cutIdentifier" "202303271415-baa69b5798";
fileInfo "osv" "Windows 10 Home v2009 (Build: 26200)";
fileInfo "UUID" "E4451D04-4686-F44A-7312-4FB29240512D";
createNode transform -n "retarget";
	rename -uid "7A051FD4-4E55-AF37-32DD-838790E09328";
	addAttr -ci true -sn "root_y_only" -ln "root_y_only" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "hand_orientation" -ln "hand_orientation" -min 0 -max 1 -en 
		"x:z" -at "enum";
	addAttr -ci true -sn "foot_offset" -ln "foot_offset" -at "long";
	addAttr -ci true -sn "foot_lock_tolerance" -ln "foot_lock_tolerance" -dv 0.2 -min 
		0.001 -at "double";
	addAttr -ci true -sn "Hip" -ln "Hip" -dt "matrix";
	addAttr -ci true -sn "Spine" -ln "Spine" -dt "matrix";
	addAttr -ci true -sn "Neck" -ln "Neck" -dt "matrix";
	addAttr -ci true -sn "Head" -ln "Head" -dt "matrix";
	addAttr -ci true -sn "LeftCollar" -ln "LeftCollar" -dt "matrix";
	addAttr -ci true -sn "RightCollar" -ln "RightCollar" -dt "matrix";
	addAttr -ci true -sn "LeftShoulder" -ln "LeftShoulder" -dt "matrix";
	addAttr -ci true -sn "RightShoulder" -ln "RightShoulder" -dt "matrix";
	addAttr -ci true -sn "LeftElbow" -ln "LeftElbow" -dt "matrix";
	addAttr -ci true -sn "RightElbow" -ln "RightElbow" -dt "matrix";
	addAttr -ci true -sn "LeftHand" -ln "LeftHand" -dt "matrix";
	addAttr -ci true -sn "RightHand" -ln "RightHand" -dt "matrix";
	addAttr -ci true -sn "LeftHip" -ln "LeftHip" -dt "matrix";
	addAttr -ci true -sn "RightHip" -ln "RightHip" -dt "matrix";
	addAttr -ci true -sn "LeftKnee" -ln "LeftKnee" -dt "matrix";
	addAttr -ci true -sn "RightKnee" -ln "RightKnee" -dt "matrix";
	addAttr -ci true -sn "LeftFoot" -ln "LeftFoot" -dt "matrix";
	addAttr -ci true -sn "RightFoot" -ln "RightFoot" -dt "matrix";
	addAttr -ci true -sn "LeftToe" -ln "LeftToe" -dt "matrix";
	addAttr -ci true -sn "RightToe" -ln "RightToe" -dt "matrix";
	addAttr -ci true -sn "left_prev" -ln "left_prev" -at "double3" -nc 3;
	addAttr -ci true -sn "left_prevX" -ln "left_prevX" -at "double" -p "left_prev";
	addAttr -ci true -sn "left_prevY" -ln "left_prevY" -at "double" -p "left_prev";
	addAttr -ci true -sn "left_prevZ" -ln "left_prevZ" -at "double" -p "left_prev";
	addAttr -ci true -sn "right_prev" -ln "right_prev" -at "double3" -nc 3;
	addAttr -ci true -sn "right_prevX" -ln "right_prevX" -at "double" -p "right_prev";
	addAttr -ci true -sn "right_prevY" -ln "right_prevY" -at "double" -p "right_prev";
	addAttr -ci true -sn "right_prevZ" -ln "right_prevZ" -at "double" -p "right_prev";
	addAttr -ci true -sn "puppeteer_node_retarget" -ln "puppeteer_node_retarget" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "clav_offset" -ln "clav_offset" -at "double";
	addAttr -ci true -sn "LeftThumb" -ln "LeftThumb" -at "matrix";
	addAttr -ci true -sn "LeftIndexFinger" -ln "LeftIndexFinger" -at "matrix";
	addAttr -ci true -sn "LeftMiddleFinger" -ln "LeftMiddleFinger" -at "matrix";
	addAttr -ci true -sn "LeftRingFinger" -ln "LeftRingFinger" -at "matrix";
	addAttr -ci true -sn "LeftPinkyFinger" -ln "LeftPinkyFinger" -at "matrix";
	addAttr -ci true -sn "RightThumb" -ln "RightThumb" -at "matrix";
	addAttr -ci true -sn "RightIndexFinger" -ln "RightIndexFinger" -at "matrix";
	addAttr -ci true -sn "RightMiddleFinger" -ln "RightMiddleFinger" -at "matrix";
	addAttr -ci true -sn "RightRingFinger" -ln "RightRingFinger" -at "matrix";
	addAttr -ci true -sn "RightPinkyFinger" -ln "RightPinkyFinger" -at "matrix";
	addAttr -ci true -sn "LeftThumb1" -ln "LeftThumb1" -at "matrix";
	addAttr -ci true -sn "LeftThumb2" -ln "LeftThumb2" -at "matrix";
	addAttr -ci true -sn "LeftIndexFinger1" -ln "LeftIndexFinger1" -at "matrix";
	addAttr -ci true -sn "LeftIndexFinger2" -ln "LeftIndexFinger2" -at "matrix";
	addAttr -ci true -sn "LeftMiddleFinger1" -ln "LeftMiddleFinger1" -at "matrix";
	addAttr -ci true -sn "LeftMiddleFinger2" -ln "LeftMiddleFinger2" -at "matrix";
	addAttr -ci true -sn "LeftRingFinger1" -ln "LeftRingFinger1" -at "matrix";
	addAttr -ci true -sn "LeftRingFinger2" -ln "LeftRingFinger2" -at "matrix";
	addAttr -ci true -sn "LeftPinkyFinger1" -ln "LeftPinkyFinger1" -at "matrix";
	addAttr -ci true -sn "LeftPinkyFinger2" -ln "LeftPinkyFinger2" -at "matrix";
	addAttr -ci true -sn "RightThumb1" -ln "RightThumb1" -at "matrix";
	addAttr -ci true -sn "RightThumb2" -ln "RightThumb2" -at "matrix";
	addAttr -ci true -sn "RightIndexFinger1" -ln "RightIndexFinger1" -at "matrix";
	addAttr -ci true -sn "RightIndexFinger2" -ln "RightIndexFinger2" -at "matrix";
	addAttr -ci true -sn "RightMiddleFinger1" -ln "RightMiddleFinger1" -at "matrix";
	addAttr -ci true -sn "RightMiddleFinger2" -ln "RightMiddleFinger2" -at "matrix";
	addAttr -ci true -sn "RightRingFinger1" -ln "RightRingFinger1" -at "matrix";
	addAttr -ci true -sn "RightRingFinger2" -ln "RightRingFinger2" -at "matrix";
	addAttr -ci true -sn "RightPinkyFinger1" -ln "RightPinkyFinger1" -at "matrix";
	addAttr -ci true -sn "RightPinkyFinger2" -ln "RightPinkyFinger2" -at "matrix";
	addAttr -ci true -sn "LeftThumb_Z" -ln "LeftThumb_Z" -at "matrix";
	addAttr -ci true -sn "LeftIndexFinger_Z" -ln "LeftIndexFinger_Z" -at "matrix";
	addAttr -ci true -sn "LeftMiddleFinger_Z" -ln "LeftMiddleFinger_Z" -at "matrix";
	addAttr -ci true -sn "LeftRingFinger_Z" -ln "LeftRingFinger_Z" -at "matrix";
	addAttr -ci true -sn "LeftPinkyFinger_Z" -ln "LeftPinkyFinger_Z" -at "matrix";
	addAttr -ci true -sn "RightThumb_Z" -ln "RightThumb_Z" -at "matrix";
	addAttr -ci true -sn "RightIndexFinger_Z" -ln "RightIndexFinger_Z" -at "matrix";
	addAttr -ci true -sn "RightMiddleFinger_Z" -ln "RightMiddleFinger_Z" -at "matrix";
	addAttr -ci true -sn "RightRingFinger_Z" -ln "RightRingFinger_Z" -at "matrix";
	addAttr -ci true -sn "RightPinkyFinger_Z" -ln "RightPinkyFinger_Z" -at "matrix";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr -k on ".root_y_only" yes;
	setAttr -k on ".hand_orientation" 1;
	setAttr -k on ".foot_offset" -25;
	setAttr -k on ".foot_lock_tolerance" 0.001;
	setAttr -k on ".Hip" -type "matrix" 0.4425093941842328 0.0051744166503092208 -0.89674894004434902 0
		 -0.12046784569212676 0.99126232110544654 -0.053726240428416623 0 0.88863543380434284 0.13180377903764029 0.43926624001668468 0
		 5.3906002044667796 86.515266418441087 -4.3958001136771685 1;
	setAttr -k on ".Spine" -type "matrix" 0.21690087681547432 -0.13723272039804912 -0.96649945167519902 0
		 0.15229809187089371 0.98270322956304346 -0.1053548946109323 0 0.96424027132701451 -0.12434445326650766 0.23404947360054029 0
		 8.3818055741970028 109.60258189421322 -5.2697096147700728 1;
	setAttr -k on ".Neck" -type "matrix" 0.13077424545807931 -0.12997982292957533 -0.98285469035646233 0
		 0.32568106677025677 0.94198288037000677 -0.081240973879223924 0 0.93639197960677178 -0.30947293697616507 0.1655190678051594 0
		 9.080003297912782 130.45600864099424 -8.0739871978018645 1;
	setAttr -k on ".Head" -type "matrix" 0.10968919312559613 -0.049766856577126012 -0.99271926590427295 0
		 0.37154287348570691 0.92839956981338068 -0.0054892560466140994 0 0.92191332242953894 -0.36823565655215007 0.12032592060801883 0
		 12.591185210797155 140.6115675274894 -8.9498497123123162 1;
	setAttr -k on ".LeftCollar" -type "matrix" 0.37083431901868275 -0.22286467082214467 -0.90156155992639686 0
		 0.025644959374999721 0.97286622932470945 -0.22994267959169321 0 0.92834489490503247 0.062150127421354395 0.36648754107732628 0
		 9.5931333700147832 126.92835578752099 -9.8251204828765513 1;
	setAttr -k on ".RightCollar" -type "matrix" -0.12156547479706459 -0.10266471400425828 -0.98725973878985818 0
		 0.061970037348400106 0.99191114404517733 -0.11077904490316108 0 0.99064703593562198 -0.074647430076611149 -0.11422001302116588 0
		 8.6006122677114973 127.55606495887994 -5.4026284838275274 1;
	setAttr -k on ".LeftShoulder" -type "matrix" 0.67529220171143634 -0.6991661672665449 -0.23483422420329231 0
		 0.39037067180177998 0.60896117808646744 -0.69049042149779327 0 0.62577246735884706 0.37461040312968258 0.68416070112384331 0
		 12.209151402983355 122.48341471225926 -22.338332783849918 1;
	setAttr -k on ".RightShoulder" -type "matrix" -0.51627796059769704 0.62609936899125773 -0.58434291948261241 0
		 0.46477162670152372 0.77792192665656912 0.42287682726744708 0 0.71933608446534469 -0.053264023273798984 -0.69261716800147666 0
		 7.7140197800891972 127.72838950278266 8.1016264269969938 1;
	setAttr -k on ".LeftElbow" -type "matrix" 0.70090101944998207 0.54419955558716637 0.46106898034061916 0
		 0.11718425014750405 0.54978232596433119 -0.82704730552384276 0 -0.70356635255743638 0.63370832230262886 0.321571375891954 0
		 28.787787729182472 105.31682678112075 -28.105337910565584 1;
	setAttr -k on ".RightElbow" -type "matrix" -0.4072304286211208 0.071678448330342398 0.91050841734145627 0
		 0.36526162156274578 0.92650242170453501 0.090427929250960271 0 -0.83710651999494234 0.36939878535292675 -0.40348136457756067 0
		 20.388367952610814 112.356436337785 22.449780815753783 1;
	setAttr -k on ".LeftHand" -type "matrix" 0.60920121932049243 0.79203461080215531 0.039434118089990984 0
		 0.089641781898923412 -0.01937030541125076 -0.99578569090236069 0 -0.78793288122532545 0.6101688016929292 -0.082799807513085188 0
		 45.990686572668267 118.65426828824491 -16.747347651830786 1;
	setAttr -k on ".RightHand" -type "matrix" -0.35672504623663093 -0.12134005024001325 0.9262957592447757 0
		 0.5049869369221518 0.80913965393374421 0.30046832440308002 0 -0.78596147165435992 0.57495183506043612 -0.22736524016476381 0
		 30.369560481885394 110.55525390107798 0.090022125675929487 1;
	setAttr -k on ".LeftHip" -type "matrix" 0.42667125724142491 0.24140239171652439 -0.87159424247593276 0
		 -0.56747717032334422 0.82185928714412881 -0.050169445844916144 0 0.70421679858227149 0.51601569492421206 0.48765408148199718 0
		 9.4079366916061851 78.179427204968775 -10.416238285575876 1;
	setAttr -k on ".RightHip" -type "matrix" 0.56818847339154943 -0.23426291623177847 -0.78884899998871416 0
		 -0.15819416149316329 0.90964697551948381 -0.38407940220397413 0 0.80754966780631321 0.34302079529741331 0.47979190074351469 0
		 3.0947473034598985 78.105612898567799 2.377498061262961 1;
	setAttr -k on ".LeftKnee" -type "matrix" 0.60490214573548162 0.13380557741900062 -0.78497736370917692 0
		 0.033426398006797309 0.98064554009304206 0.1929170822181081 0 0.79559793237572762 -0.1429349227684576 0.58872195292198293 0
		 31.554086848152636 45.520867502583563 -8.5650354345134119 1;
	setAttr -k on ".RightKnee" -type "matrix" 0.64192811779598336 -0.26206067500865227 -0.72059176667274438 0
		 0.57611530363839702 0.78500072625807737 0.22773892220602121 0 0.50598364449473565 -0.56133596213669767 0.65489120402974121 0
		 9.0852029733442592 42.040860962370274 17.341213327517075 1;
	setAttr -k on ".LeftFoot" -type "matrix" 0.58407412227925248 0.15656642171963883 -0.79645739074558186 0
		 -0.21658996327163776 0.97570582229223213 0.032968714786304365 0 0.78226990706107502 0.15324850385755265 0.60379523728803142 0
		 29.998029400120618 8.9946947943568247 -15.929106283762216 1;
	setAttr -k on ".RightFoot" -type "matrix" 0.73207953216894273 -0.35025965055159225 -0.58427539377797655 0
		 0.46249093692940557 0.88528101871130549 0.048781668352623209 0 0.50016166570129494 -0.30593413523923918 0.81008802796853885 0
		 -12.546734251766797 12.952023578962891 8.5829278765412056 1;
	setAttr -k on ".LeftToe";
	setAttr -k on ".RightToe";
	setAttr -k on ".left_prev";
	setAttr -k on ".right_prev";
	setAttr -k on ".clav_offset";
	setAttr ".LeftIndexFinger" -type "matrix" 0.45164979761362811 0.6589420650102058 0.60150462614620515 0
		 0.32836176982685583 0.50409735743150086 -0.79878933539850405 0 -0.829572786698898 0.55828416526917124 0.011304086781389694 0
		 49.028708330888904 126.71174801540536 -16.418582495585728 1;
	setAttr ".LeftIndexFinger1" -type "matrix" -0.046597031594001193 -0.089384931256649772 0.99490655375794113 0
		 0.55645098990555697 0.82482066541723176 0.10016569139896503 0 -0.82957278913871391 0.55828416058898811 0.011304138874572942 0
		 50.55970040935734 128.94531702742378 -14.374797404308154 1;
	setAttr ".LeftIndexFinger2" -type "matrix" -0.24338745438884776 -0.37972890137457033 0.89250686748428432 0
		 0.50256495556929071 0.73764812579979 0.45089212450133326 0 -0.82957278913871391 0.55828416058898811 0.011304138874572942 0
		 50.442305882391317 128.72012719922571 -11.868404682551496 1;
createNode nurbsCurve -n "hipsX" -p "retarget";
	rename -uid "8700C3D7-4EBA-A1BA-B331-64B6F9B0725E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "hipsY" -p "retarget";
	rename -uid "738FF4E5-49D4-4799-55D2-CBAC47A89EC4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "hipsZ" -p "retarget";
	rename -uid "6E7A7A6C-4CDB-CC07-C9D7-02AC163952F6";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "LeftLegShape" -p "retarget";
	rename -uid "2750CFEB-4B36-223E-ABB8-858D4D4B7828";
	setAttr -k off ".v";
	setAttr -s 3 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		6.8973353960592867 80.235052087285993 -0.16967440907100695
		7.7511482887158349 42.645090477249155 -0.33026612832233565
		6.7439639250290746 4.9522316701197608 -0.84308526689299068
		0 0 0
		;
createNode nurbsCurve -n "RightLegShape" -p "retarget";
	rename -uid "FFED864D-48F8-DD26-9508-949B8E16B31F";
	setAttr -k off ".v";
	setAttr -s 3 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		-8.2026472708063487 80.234069091971023 -0.16967925384998184
		-6.9328177939168025 42.657020207020871 -0.50573013941477896
		-6.7439615723370476 4.9522316701197608 -0.84308909403388921
		0 0 0
		;
createNode transform -n "clip" -p "retarget";
	rename -uid "AC255998-43D7-A332-8BF4-8B93F8374629";
	addAttr -ci true -k true -sn "Spine" -ln "Spine" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "SpineX" -ln "SpineX" -at "double" -p "Spine";
	addAttr -ci true -k true -sn "SpineY" -ln "SpineY" -at "double" -p "Spine";
	addAttr -ci true -k true -sn "SpineZ" -ln "SpineZ" -at "double" -p "Spine";
	addAttr -ci true -k true -sn "Neck" -ln "Neck" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "NeckX" -ln "NeckX" -at "double" -p "Neck";
	addAttr -ci true -k true -sn "NeckY" -ln "NeckY" -at "double" -p "Neck";
	addAttr -ci true -k true -sn "NeckZ" -ln "NeckZ" -at "double" -p "Neck";
	addAttr -ci true -k true -sn "Head" -ln "Head" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "HeadX" -ln "HeadX" -at "double" -p "Head";
	addAttr -ci true -k true -sn "HeadY" -ln "HeadY" -at "double" -p "Head";
	addAttr -ci true -k true -sn "HeadZ" -ln "HeadZ" -at "double" -p "Head";
	addAttr -ci true -k true -sn "Head_Z" -ln "Head_Z" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "Head_ZX" -ln "Head_ZX" -at "double" -p "Head_Z";
	addAttr -ci true -k true -sn "Head_ZY" -ln "Head_ZY" -at "double" -p "Head_Z";
	addAttr -ci true -k true -sn "Head_ZZ" -ln "Head_ZZ" -at "double" -p "Head_Z";
	addAttr -ci true -k true -sn "LeftHip" -ln "LeftHip" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftHipX" -ln "LeftHipX" -at "double" -p "LeftHip";
	addAttr -ci true -k true -sn "LeftHipY" -ln "LeftHipY" -at "double" -p "LeftHip";
	addAttr -ci true -k true -sn "LeftHipZ" -ln "LeftHipZ" -at "double" -p "LeftHip";
	addAttr -ci true -k true -sn "LeftKnee" -ln "LeftKnee" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftKneeX" -ln "LeftKneeX" -at "double" -p "LeftKnee";
	addAttr -ci true -k true -sn "LeftKneeY" -ln "LeftKneeY" -at "double" -p "LeftKnee";
	addAttr -ci true -k true -sn "LeftKneeZ" -ln "LeftKneeZ" -at "double" -p "LeftKnee";
	addAttr -ci true -k true -sn "LeftFoot" -ln "LeftFoot" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftFootX" -ln "LeftFootX" -at "double" -p "LeftFoot";
	addAttr -ci true -k true -sn "LeftFootY" -ln "LeftFootY" -at "double" -p "LeftFoot";
	addAttr -ci true -k true -sn "LeftFootZ" -ln "LeftFootZ" -at "double" -p "LeftFoot";
	addAttr -ci true -k true -sn "LeftToe" -ln "LeftToe" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftToeX" -ln "LeftToeX" -at "double" -p "LeftToe";
	addAttr -ci true -k true -sn "LeftToeY" -ln "LeftToeY" -at "double" -p "LeftToe";
	addAttr -ci true -k true -sn "LeftToeZ" -ln "LeftToeZ" -at "double" -p "LeftToe";
	addAttr -ci true -k true -sn "LeftCollar" -ln "LeftCollar" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftCollarX" -ln "LeftCollarX" -at "double" -p "LeftCollar";
	addAttr -ci true -k true -sn "LeftCollarY" -ln "LeftCollarY" -at "double" -p "LeftCollar";
	addAttr -ci true -k true -sn "LeftCollarZ" -ln "LeftCollarZ" -at "double" -p "LeftCollar";
	addAttr -ci true -k true -sn "LeftShoulder" -ln "LeftShoulder" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "LeftShoulderX" -ln "LeftShoulderX" -at "double" -p "LeftShoulder";
	addAttr -ci true -k true -sn "LeftShoulderY" -ln "LeftShoulderY" -at "double" -p "LeftShoulder";
	addAttr -ci true -k true -sn "LeftShoulderZ" -ln "LeftShoulderZ" -at "double" -p "LeftShoulder";
	addAttr -ci true -k true -sn "LeftElbow" -ln "LeftElbow" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftElbowX" -ln "LeftElbowX" -at "double" -p "LeftElbow";
	addAttr -ci true -k true -sn "LeftElbowY" -ln "LeftElbowY" -at "double" -p "LeftElbow";
	addAttr -ci true -k true -sn "LeftElbowZ" -ln "LeftElbowZ" -at "double" -p "LeftElbow";
	addAttr -ci true -k true -sn "LeftHand" -ln "LeftHand" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftHandX" -ln "LeftHandX" -at "double" -p "LeftHand";
	addAttr -ci true -k true -sn "LeftHandY" -ln "LeftHandY" -at "double" -p "LeftHand";
	addAttr -ci true -k true -sn "LeftHandZ" -ln "LeftHandZ" -at "double" -p "LeftHand";
	addAttr -ci true -k true -sn "LeftThumb" -ln "LeftThumb" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftThumbX" -ln "LeftThumbX" -at "double" -p "LeftThumb";
	addAttr -ci true -k true -sn "LeftThumbY" -ln "LeftThumbY" -at "double" -p "LeftThumb";
	addAttr -ci true -k true -sn "LeftThumbZ" -ln "LeftThumbZ" -at "double" -p "LeftThumb";
	addAttr -ci true -k true -sn "LeftIndexFinger" -ln "LeftIndexFinger" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftIndexFingerX" -ln "LeftIndexFingerX" -at "double" 
		-p "LeftIndexFinger";
	addAttr -ci true -k true -sn "LeftIndexFingerY" -ln "LeftIndexFingerY" -at "double" 
		-p "LeftIndexFinger";
	addAttr -ci true -k true -sn "LeftIndexFingerZ" -ln "LeftIndexFingerZ" -at "double" 
		-p "LeftIndexFinger";
	addAttr -ci true -k true -sn "LeftMiddleFinger" -ln "LeftMiddleFinger" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftMiddleFingerX" -ln "LeftMiddleFingerX" -at "double" 
		-p "LeftMiddleFinger";
	addAttr -ci true -k true -sn "LeftMiddleFingerY" -ln "LeftMiddleFingerY" -at "double" 
		-p "LeftMiddleFinger";
	addAttr -ci true -k true -sn "LeftMiddleFingerZ" -ln "LeftMiddleFingerZ" -at "double" 
		-p "LeftMiddleFinger";
	addAttr -ci true -k true -sn "LeftRingFinger" -ln "LeftRingFinger" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftRingFingerX" -ln "LeftRingFingerX" -at "double" 
		-p "LeftRingFinger";
	addAttr -ci true -k true -sn "LeftRingFingerY" -ln "LeftRingFingerY" -at "double" 
		-p "LeftRingFinger";
	addAttr -ci true -k true -sn "LeftRingFingerZ" -ln "LeftRingFingerZ" -at "double" 
		-p "LeftRingFinger";
	addAttr -ci true -k true -sn "LeftPinkyFinger" -ln "LeftPinkyFinger" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftPinkyFingerX" -ln "LeftPinkyFingerX" -at "double" 
		-p "LeftPinkyFinger";
	addAttr -ci true -k true -sn "LeftPinkyFingerY" -ln "LeftPinkyFingerY" -at "double" 
		-p "LeftPinkyFinger";
	addAttr -ci true -k true -sn "LeftPinkyFingerZ" -ln "LeftPinkyFingerZ" -at "double" 
		-p "LeftPinkyFinger";
	addAttr -ci true -k true -sn "LeftBigToe" -ln "LeftBigToe" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftBigToeX" -ln "LeftBigToeX" -at "double" -p "LeftBigToe";
	addAttr -ci true -k true -sn "LeftBigToeY" -ln "LeftBigToeY" -at "double" -p "LeftBigToe";
	addAttr -ci true -k true -sn "LeftBigToeZ" -ln "LeftBigToeZ" -at "double" -p "LeftBigToe";
	addAttr -ci true -k true -sn "LeftIndexToe" -ln "LeftIndexToe" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "LeftIndexToeX" -ln "LeftIndexToeX" -at "double" -p "LeftIndexToe";
	addAttr -ci true -k true -sn "LeftIndexToeY" -ln "LeftIndexToeY" -at "double" -p "LeftIndexToe";
	addAttr -ci true -k true -sn "LeftIndexToeZ" -ln "LeftIndexToeZ" -at "double" -p "LeftIndexToe";
	addAttr -ci true -k true -sn "LeftMiddleToe" -ln "LeftMiddleToe" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "LeftMiddleToeX" -ln "LeftMiddleToeX" -at "double" 
		-p "LeftMiddleToe";
	addAttr -ci true -k true -sn "LeftMiddleToeY" -ln "LeftMiddleToeY" -at "double" 
		-p "LeftMiddleToe";
	addAttr -ci true -k true -sn "LeftMiddleToeZ" -ln "LeftMiddleToeZ" -at "double" 
		-p "LeftMiddleToe";
	addAttr -ci true -k true -sn "LeftRingToe" -ln "LeftRingToe" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftRingToeX" -ln "LeftRingToeX" -at "double" -p "LeftRingToe";
	addAttr -ci true -k true -sn "LeftRingToeY" -ln "LeftRingToeY" -at "double" -p "LeftRingToe";
	addAttr -ci true -k true -sn "LeftRingToeZ" -ln "LeftRingToeZ" -at "double" -p "LeftRingToe";
	addAttr -ci true -k true -sn "LeftPinkyToe" -ln "LeftPinkyToe" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "LeftPinkyToeX" -ln "LeftPinkyToeX" -at "double" -p "LeftPinkyToe";
	addAttr -ci true -k true -sn "LeftPinkyToeY" -ln "LeftPinkyToeY" -at "double" -p "LeftPinkyToe";
	addAttr -ci true -k true -sn "LeftPinkyToeZ" -ln "LeftPinkyToeZ" -at "double" -p "LeftPinkyToe";
	addAttr -ci true -k true -sn "LeftCollar_Z" -ln "LeftCollar_Z" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "LeftCollar_ZX" -ln "LeftCollar_ZX" -at "double" -p "LeftCollar_Z";
	addAttr -ci true -k true -sn "LeftCollar_ZY" -ln "LeftCollar_ZY" -at "double" -p "LeftCollar_Z";
	addAttr -ci true -k true -sn "LeftCollar_ZZ" -ln "LeftCollar_ZZ" -at "double" -p "LeftCollar_Z";
	addAttr -ci true -k true -sn "LeftHand_Z" -ln "LeftHand_Z" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftHand_ZX" -ln "LeftHand_ZX" -at "double" -p "LeftHand_Z";
	addAttr -ci true -k true -sn "LeftHand_ZY" -ln "LeftHand_ZY" -at "double" -p "LeftHand_Z";
	addAttr -ci true -k true -sn "LeftHand_ZZ" -ln "LeftHand_ZZ" -at "double" -p "LeftHand_Z";
	addAttr -ci true -k true -sn "RightHip" -ln "RightHip" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightHipX" -ln "RightHipX" -at "double" -p "RightHip";
	addAttr -ci true -k true -sn "RightHipY" -ln "RightHipY" -at "double" -p "RightHip";
	addAttr -ci true -k true -sn "RightHipZ" -ln "RightHipZ" -at "double" -p "RightHip";
	addAttr -ci true -k true -sn "RightKnee" -ln "RightKnee" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightKneeX" -ln "RightKneeX" -at "double" -p "RightKnee";
	addAttr -ci true -k true -sn "RightKneeY" -ln "RightKneeY" -at "double" -p "RightKnee";
	addAttr -ci true -k true -sn "RightKneeZ" -ln "RightKneeZ" -at "double" -p "RightKnee";
	addAttr -ci true -k true -sn "RightFoot" -ln "RightFoot" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightFootX" -ln "RightFootX" -at "double" -p "RightFoot";
	addAttr -ci true -k true -sn "RightFootY" -ln "RightFootY" -at "double" -p "RightFoot";
	addAttr -ci true -k true -sn "RightFootZ" -ln "RightFootZ" -at "double" -p "RightFoot";
	addAttr -ci true -k true -sn "RightToe" -ln "RightToe" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightToeX" -ln "RightToeX" -at "double" -p "RightToe";
	addAttr -ci true -k true -sn "RightToeY" -ln "RightToeY" -at "double" -p "RightToe";
	addAttr -ci true -k true -sn "RightToeZ" -ln "RightToeZ" -at "double" -p "RightToe";
	addAttr -ci true -k true -sn "RightCollar" -ln "RightCollar" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightCollarX" -ln "RightCollarX" -at "double" -p "RightCollar";
	addAttr -ci true -k true -sn "RightCollarY" -ln "RightCollarY" -at "double" -p "RightCollar";
	addAttr -ci true -k true -sn "RightCollarZ" -ln "RightCollarZ" -at "double" -p "RightCollar";
	addAttr -ci true -k true -sn "RightShoulder" -ln "RightShoulder" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "RightShoulderX" -ln "RightShoulderX" -at "double" 
		-p "RightShoulder";
	addAttr -ci true -k true -sn "RightShoulderY" -ln "RightShoulderY" -at "double" 
		-p "RightShoulder";
	addAttr -ci true -k true -sn "RightShoulderZ" -ln "RightShoulderZ" -at "double" 
		-p "RightShoulder";
	addAttr -ci true -k true -sn "RightElbow" -ln "RightElbow" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightElbowX" -ln "RightElbowX" -at "double" -p "RightElbow";
	addAttr -ci true -k true -sn "RightElbowY" -ln "RightElbowY" -at "double" -p "RightElbow";
	addAttr -ci true -k true -sn "RightElbowZ" -ln "RightElbowZ" -at "double" -p "RightElbow";
	addAttr -ci true -k true -sn "RightHand" -ln "RightHand" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightHandX" -ln "RightHandX" -at "double" -p "RightHand";
	addAttr -ci true -k true -sn "RightHandY" -ln "RightHandY" -at "double" -p "RightHand";
	addAttr -ci true -k true -sn "RightHandZ" -ln "RightHandZ" -at "double" -p "RightHand";
	addAttr -ci true -k true -sn "RightThumb" -ln "RightThumb" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightThumbX" -ln "RightThumbX" -at "double" -p "RightThumb";
	addAttr -ci true -k true -sn "RightThumbY" -ln "RightThumbY" -at "double" -p "RightThumb";
	addAttr -ci true -k true -sn "RightThumbZ" -ln "RightThumbZ" -at "double" -p "RightThumb";
	addAttr -ci true -k true -sn "RightIndexFinger" -ln "RightIndexFinger" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightIndexFingerX" -ln "RightIndexFingerX" -at "double" 
		-p "RightIndexFinger";
	addAttr -ci true -k true -sn "RightIndexFingerY" -ln "RightIndexFingerY" -at "double" 
		-p "RightIndexFinger";
	addAttr -ci true -k true -sn "RightIndexFingerZ" -ln "RightIndexFingerZ" -at "double" 
		-p "RightIndexFinger";
	addAttr -ci true -k true -sn "RightMiddleFinger" -ln "RightMiddleFinger" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightMiddleFingerX" -ln "RightMiddleFingerX" -at "double" 
		-p "RightMiddleFinger";
	addAttr -ci true -k true -sn "RightMiddleFingerY" -ln "RightMiddleFingerY" -at "double" 
		-p "RightMiddleFinger";
	addAttr -ci true -k true -sn "RightMiddleFingerZ" -ln "RightMiddleFingerZ" -at "double" 
		-p "RightMiddleFinger";
	addAttr -ci true -k true -sn "RightRingFinger" -ln "RightRingFinger" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightRingFingerX" -ln "RightRingFingerX" -at "double" 
		-p "RightRingFinger";
	addAttr -ci true -k true -sn "RightRingFingerY" -ln "RightRingFingerY" -at "double" 
		-p "RightRingFinger";
	addAttr -ci true -k true -sn "RightRingFingerZ" -ln "RightRingFingerZ" -at "double" 
		-p "RightRingFinger";
	addAttr -ci true -k true -sn "RightPinkyFinger" -ln "RightPinkyFinger" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightPinkyFingerX" -ln "RightPinkyFingerX" -at "double" 
		-p "RightPinkyFinger";
	addAttr -ci true -k true -sn "RightPinkyFingerY" -ln "RightPinkyFingerY" -at "double" 
		-p "RightPinkyFinger";
	addAttr -ci true -k true -sn "RightPinkyFingerZ" -ln "RightPinkyFingerZ" -at "double" 
		-p "RightPinkyFinger";
	addAttr -ci true -k true -sn "RightBigToe" -ln "RightBigToe" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightBigToeX" -ln "RightBigToeX" -at "double" -p "RightBigToe";
	addAttr -ci true -k true -sn "RightBigToeY" -ln "RightBigToeY" -at "double" -p "RightBigToe";
	addAttr -ci true -k true -sn "RightBigToeZ" -ln "RightBigToeZ" -at "double" -p "RightBigToe";
	addAttr -ci true -k true -sn "RightIndexToe" -ln "RightIndexToe" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "RightIndexToeX" -ln "RightIndexToeX" -at "double" 
		-p "RightIndexToe";
	addAttr -ci true -k true -sn "RightIndexToeY" -ln "RightIndexToeY" -at "double" 
		-p "RightIndexToe";
	addAttr -ci true -k true -sn "RightIndexToeZ" -ln "RightIndexToeZ" -at "double" 
		-p "RightIndexToe";
	addAttr -ci true -k true -sn "RightMiddleToe" -ln "RightMiddleToe" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightMiddleToeX" -ln "RightMiddleToeX" -at "double" 
		-p "RightMiddleToe";
	addAttr -ci true -k true -sn "RightMiddleToeY" -ln "RightMiddleToeY" -at "double" 
		-p "RightMiddleToe";
	addAttr -ci true -k true -sn "RightMiddleToeZ" -ln "RightMiddleToeZ" -at "double" 
		-p "RightMiddleToe";
	addAttr -ci true -k true -sn "RightRingToe" -ln "RightRingToe" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "RightRingToeX" -ln "RightRingToeX" -at "double" -p "RightRingToe";
	addAttr -ci true -k true -sn "RightRingToeY" -ln "RightRingToeY" -at "double" -p "RightRingToe";
	addAttr -ci true -k true -sn "RightRingToeZ" -ln "RightRingToeZ" -at "double" -p "RightRingToe";
	addAttr -ci true -k true -sn "RightPinkyToe" -ln "RightPinkyToe" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "RightPinkyToeX" -ln "RightPinkyToeX" -at "double" 
		-p "RightPinkyToe";
	addAttr -ci true -k true -sn "RightPinkyToeY" -ln "RightPinkyToeY" -at "double" 
		-p "RightPinkyToe";
	addAttr -ci true -k true -sn "RightPinkyToeZ" -ln "RightPinkyToeZ" -at "double" 
		-p "RightPinkyToe";
	addAttr -ci true -k true -sn "RightCollar_Z" -ln "RightCollar_Z" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "RightCollar_ZX" -ln "RightCollar_ZX" -at "double" 
		-p "RightCollar_Z";
	addAttr -ci true -k true -sn "RightCollar_ZY" -ln "RightCollar_ZY" -at "double" 
		-p "RightCollar_Z";
	addAttr -ci true -k true -sn "RightCollar_ZZ" -ln "RightCollar_ZZ" -at "double" 
		-p "RightCollar_Z";
	addAttr -ci true -k true -sn "RightHand_Z" -ln "RightHand_Z" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightHand_ZX" -ln "RightHand_ZX" -at "double" -p "RightHand_Z";
	addAttr -ci true -k true -sn "RightHand_ZY" -ln "RightHand_ZY" -at "double" -p "RightHand_Z";
	addAttr -ci true -k true -sn "RightHand_ZZ" -ln "RightHand_ZZ" -at "double" -p "RightHand_Z";
	addAttr -ci true -k true -sn "Spine_Z" -ln "Spine_Z" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "Spine_ZX" -ln "Spine_ZX" -at "double" -p "Spine_Z";
	addAttr -ci true -k true -sn "Spine_ZY" -ln "Spine_ZY" -at "double" -p "Spine_Z";
	addAttr -ci true -k true -sn "Spine_ZZ" -ln "Spine_ZZ" -at "double" -p "Spine_Z";
	addAttr -ci true -k true -sn "Hip_Z" -ln "Hip_Z" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "Hip_ZX" -ln "Hip_ZX" -at "double" -p "Hip_Z";
	addAttr -ci true -k true -sn "Hip_ZY" -ln "Hip_ZY" -at "double" -p "Hip_Z";
	addAttr -ci true -k true -sn "Hip_ZZ" -ln "Hip_ZZ" -at "double" -p "Hip_Z";
	addAttr -ci true -k true -sn "LeftToe_X" -ln "LeftToe_X" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftToe_XX" -ln "LeftToe_XX" -at "double" -p "LeftToe_X";
	addAttr -ci true -k true -sn "LeftToe_XY" -ln "LeftToe_XY" -at "double" -p "LeftToe_X";
	addAttr -ci true -k true -sn "LeftToe_XZ" -ln "LeftToe_XZ" -at "double" -p "LeftToe_X";
	addAttr -ci true -k true -sn "LeftToe_Y" -ln "LeftToe_Y" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftToe_YX" -ln "LeftToe_YX" -at "double" -p "LeftToe_Y";
	addAttr -ci true -k true -sn "LeftToe_YY" -ln "LeftToe_YY" -at "double" -p "LeftToe_Y";
	addAttr -ci true -k true -sn "LeftToe_YZ" -ln "LeftToe_YZ" -at "double" -p "LeftToe_Y";
	addAttr -ci true -k true -sn "RightToe_X" -ln "RightToe_X" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightToe_XX" -ln "RightToe_XX" -at "double" -p "RightToe_X";
	addAttr -ci true -k true -sn "RightToe_XY" -ln "RightToe_XY" -at "double" -p "RightToe_X";
	addAttr -ci true -k true -sn "RightToe_XZ" -ln "RightToe_XZ" -at "double" -p "RightToe_X";
	addAttr -ci true -k true -sn "RightToe_Y" -ln "RightToe_Y" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightToe_YX" -ln "RightToe_YX" -at "double" -p "RightToe_Y";
	addAttr -ci true -k true -sn "RightToe_YY" -ln "RightToe_YY" -at "double" -p "RightToe_Y";
	addAttr -ci true -k true -sn "RightToe_YZ" -ln "RightToe_YZ" -at "double" -p "RightToe_Y";
	addAttr -ci true -sn "thigh_length" -ln "thigh_length" -at "double";
	addAttr -ci true -sn "shin_length" -ln "shin_length" -at "double";
	addAttr -ci true -sn "hip_width" -ln "hip_width" -at "double";
	addAttr -ci true -k true -sn "LeftThumb1" -ln "LeftThumb1" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftThumb1X" -ln "LeftThumb1X" -at "double" -p "LeftThumb1";
	addAttr -ci true -k true -sn "LeftThumb1Y" -ln "LeftThumb1Y" -at "double" -p "LeftThumb1";
	addAttr -ci true -k true -sn "LeftThumb1Z" -ln "LeftThumb1Z" -at "double" -p "LeftThumb1";
	addAttr -ci true -k true -sn "LeftThumb2" -ln "LeftThumb2" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftThumb2X" -ln "LeftThumb2X" -at "double" -p "LeftThumb2";
	addAttr -ci true -k true -sn "LeftThumb2Y" -ln "LeftThumb2Y" -at "double" -p "LeftThumb2";
	addAttr -ci true -k true -sn "LeftThumb2Z" -ln "LeftThumb2Z" -at "double" -p "LeftThumb2";
	addAttr -ci true -k true -sn "LeftIndexFinger1" -ln "LeftIndexFinger1" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftIndexFinger1X" -ln "LeftIndexFinger1X" -at "double" 
		-p "LeftIndexFinger1";
	addAttr -ci true -k true -sn "LeftIndexFinger1Y" -ln "LeftIndexFinger1Y" -at "double" 
		-p "LeftIndexFinger1";
	addAttr -ci true -k true -sn "LeftIndexFinger1Z" -ln "LeftIndexFinger1Z" -at "double" 
		-p "LeftIndexFinger1";
	addAttr -ci true -k true -sn "LeftIndexFinger2" -ln "LeftIndexFinger2" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftIndexFinger2X" -ln "LeftIndexFinger2X" -at "double" 
		-p "LeftIndexFinger2";
	addAttr -ci true -k true -sn "LeftIndexFinger2Y" -ln "LeftIndexFinger2Y" -at "double" 
		-p "LeftIndexFinger2";
	addAttr -ci true -k true -sn "LeftIndexFinger2Z" -ln "LeftIndexFinger2Z" -at "double" 
		-p "LeftIndexFinger2";
	addAttr -ci true -k true -sn "LeftMiddleFinger1" -ln "LeftMiddleFinger1" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftMiddleFinger1X" -ln "LeftMiddleFinger1X" -at "double" 
		-p "LeftMiddleFinger1";
	addAttr -ci true -k true -sn "LeftMiddleFinger1Y" -ln "LeftMiddleFinger1Y" -at "double" 
		-p "LeftMiddleFinger1";
	addAttr -ci true -k true -sn "LeftMiddleFinger1Z" -ln "LeftMiddleFinger1Z" -at "double" 
		-p "LeftMiddleFinger1";
	addAttr -ci true -k true -sn "LeftMiddleFinger2" -ln "LeftMiddleFinger2" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftMiddleFinger2X" -ln "LeftMiddleFinger2X" -at "double" 
		-p "LeftMiddleFinger2";
	addAttr -ci true -k true -sn "LeftMiddleFinger2Y" -ln "LeftMiddleFinger2Y" -at "double" 
		-p "LeftMiddleFinger2";
	addAttr -ci true -k true -sn "LeftMiddleFinger2Z" -ln "LeftMiddleFinger2Z" -at "double" 
		-p "LeftMiddleFinger2";
	addAttr -ci true -k true -sn "LeftRingFinger1" -ln "LeftRingFinger1" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftRingFinger1X" -ln "LeftRingFinger1X" -at "double" 
		-p "LeftRingFinger1";
	addAttr -ci true -k true -sn "LeftRingFinger1Y" -ln "LeftRingFinger1Y" -at "double" 
		-p "LeftRingFinger1";
	addAttr -ci true -k true -sn "LeftRingFinger1Z" -ln "LeftRingFinger1Z" -at "double" 
		-p "LeftRingFinger1";
	addAttr -ci true -k true -sn "LeftRingFinger2" -ln "LeftRingFinger2" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftRingFinger2X" -ln "LeftRingFinger2X" -at "double" 
		-p "LeftRingFinger2";
	addAttr -ci true -k true -sn "LeftRingFinger2Y" -ln "LeftRingFinger2Y" -at "double" 
		-p "LeftRingFinger2";
	addAttr -ci true -k true -sn "LeftRingFinger2Z" -ln "LeftRingFinger2Z" -at "double" 
		-p "LeftRingFinger2";
	addAttr -ci true -k true -sn "LeftPinkyFinger1" -ln "LeftPinkyFinger1" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftPinkyFinger1X" -ln "LeftPinkyFinger1X" -at "double" 
		-p "LeftPinkyFinger1";
	addAttr -ci true -k true -sn "LeftPinkyFinger1Y" -ln "LeftPinkyFinger1Y" -at "double" 
		-p "LeftPinkyFinger1";
	addAttr -ci true -k true -sn "LeftPinkyFinger1Z" -ln "LeftPinkyFinger1Z" -at "double" 
		-p "LeftPinkyFinger1";
	addAttr -ci true -k true -sn "LeftPinkyFinger2" -ln "LeftPinkyFinger2" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftPinkyFinger2X" -ln "LeftPinkyFinger2X" -at "double" 
		-p "LeftPinkyFinger2";
	addAttr -ci true -k true -sn "LeftPinkyFinger2Y" -ln "LeftPinkyFinger2Y" -at "double" 
		-p "LeftPinkyFinger2";
	addAttr -ci true -k true -sn "LeftPinkyFinger2Z" -ln "LeftPinkyFinger2Z" -at "double" 
		-p "LeftPinkyFinger2";
	addAttr -ci true -k true -sn "RightThumb1" -ln "RightThumb1" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightThumb1X" -ln "RightThumb1X" -at "double" -p "RightThumb1";
	addAttr -ci true -k true -sn "RightThumb1Y" -ln "RightThumb1Y" -at "double" -p "RightThumb1";
	addAttr -ci true -k true -sn "RightThumb1Z" -ln "RightThumb1Z" -at "double" -p "RightThumb1";
	addAttr -ci true -k true -sn "RightThumb2" -ln "RightThumb2" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "RightThumb2X" -ln "RightThumb2X" -at "double" -p "RightThumb2";
	addAttr -ci true -k true -sn "RightThumb2Y" -ln "RightThumb2Y" -at "double" -p "RightThumb2";
	addAttr -ci true -k true -sn "RightThumb2Z" -ln "RightThumb2Z" -at "double" -p "RightThumb2";
	addAttr -ci true -k true -sn "RightIndexFinger1" -ln "RightIndexFinger1" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightIndexFinger1X" -ln "RightIndexFinger1X" -at "double" 
		-p "RightIndexFinger1";
	addAttr -ci true -k true -sn "RightIndexFinger1Y" -ln "RightIndexFinger1Y" -at "double" 
		-p "RightIndexFinger1";
	addAttr -ci true -k true -sn "RightIndexFinger1Z" -ln "RightIndexFinger1Z" -at "double" 
		-p "RightIndexFinger1";
	addAttr -ci true -k true -sn "RightIndexFinger2" -ln "RightIndexFinger2" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightIndexFinger2X" -ln "RightIndexFinger2X" -at "double" 
		-p "RightIndexFinger2";
	addAttr -ci true -k true -sn "RightIndexFinger2Y" -ln "RightIndexFinger2Y" -at "double" 
		-p "RightIndexFinger2";
	addAttr -ci true -k true -sn "RightIndexFinger2Z" -ln "RightIndexFinger2Z" -at "double" 
		-p "RightIndexFinger2";
	addAttr -ci true -k true -sn "RightMiddleFinger1" -ln "RightMiddleFinger1" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightMiddleFinger1X" -ln "RightMiddleFinger1X" -at "double" 
		-p "RightMiddleFinger1";
	addAttr -ci true -k true -sn "RightMiddleFinger1Y" -ln "RightMiddleFinger1Y" -at "double" 
		-p "RightMiddleFinger1";
	addAttr -ci true -k true -sn "RightMiddleFinger1Z" -ln "RightMiddleFinger1Z" -at "double" 
		-p "RightMiddleFinger1";
	addAttr -ci true -k true -sn "RightMiddleFinger2" -ln "RightMiddleFinger2" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightMiddleFinger2X" -ln "RightMiddleFinger2X" -at "double" 
		-p "RightMiddleFinger2";
	addAttr -ci true -k true -sn "RightMiddleFinger2Y" -ln "RightMiddleFinger2Y" -at "double" 
		-p "RightMiddleFinger2";
	addAttr -ci true -k true -sn "RightMiddleFinger2Z" -ln "RightMiddleFinger2Z" -at "double" 
		-p "RightMiddleFinger2";
	addAttr -ci true -k true -sn "RightRingFinger1" -ln "RightRingFinger1" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightRingFinger1X" -ln "RightRingFinger1X" -at "double" 
		-p "RightRingFinger1";
	addAttr -ci true -k true -sn "RightRingFinger1Y" -ln "RightRingFinger1Y" -at "double" 
		-p "RightRingFinger1";
	addAttr -ci true -k true -sn "RightRingFinger1Z" -ln "RightRingFinger1Z" -at "double" 
		-p "RightRingFinger1";
	addAttr -ci true -k true -sn "RightRingFinger2" -ln "RightRingFinger2" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightRingFinger2X" -ln "RightRingFinger2X" -at "double" 
		-p "RightRingFinger2";
	addAttr -ci true -k true -sn "RightRingFinger2Y" -ln "RightRingFinger2Y" -at "double" 
		-p "RightRingFinger2";
	addAttr -ci true -k true -sn "RightRingFinger2Z" -ln "RightRingFinger2Z" -at "double" 
		-p "RightRingFinger2";
	addAttr -ci true -k true -sn "RightPinkyFinger1" -ln "RightPinkyFinger1" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightPinkyFinger1X" -ln "RightPinkyFinger1X" -at "double" 
		-p "RightPinkyFinger1";
	addAttr -ci true -k true -sn "RightPinkyFinger1Y" -ln "RightPinkyFinger1Y" -at "double" 
		-p "RightPinkyFinger1";
	addAttr -ci true -k true -sn "RightPinkyFinger1Z" -ln "RightPinkyFinger1Z" -at "double" 
		-p "RightPinkyFinger1";
	addAttr -ci true -k true -sn "RightPinkyFinger2" -ln "RightPinkyFinger2" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightPinkyFinger2X" -ln "RightPinkyFinger2X" -at "double" 
		-p "RightPinkyFinger2";
	addAttr -ci true -k true -sn "RightPinkyFinger2Y" -ln "RightPinkyFinger2Y" -at "double" 
		-p "RightPinkyFinger2";
	addAttr -ci true -k true -sn "RightPinkyFinger2Z" -ln "RightPinkyFinger2Z" -at "double" 
		-p "RightPinkyFinger2";
	addAttr -ci true -k true -sn "LeftThumb_Z" -ln "LeftThumb_Z" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "LeftThumb_ZX" -ln "LeftThumb_ZX" -at "double" -p "LeftThumb_Z";
	addAttr -ci true -k true -sn "LeftThumb_ZY" -ln "LeftThumb_ZY" -at "double" -p "LeftThumb_Z";
	addAttr -ci true -k true -sn "LeftThumb_ZZ" -ln "LeftThumb_ZZ" -at "double" -p "LeftThumb_Z";
	addAttr -ci true -k true -sn "LeftIndexFinger_Z" -ln "LeftIndexFinger_Z" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftIndexFinger_ZX" -ln "LeftIndexFinger_ZX" -at "double" 
		-p "LeftIndexFinger_Z";
	addAttr -ci true -k true -sn "LeftIndexFinger_ZY" -ln "LeftIndexFinger_ZY" -at "double" 
		-p "LeftIndexFinger_Z";
	addAttr -ci true -k true -sn "LeftIndexFinger_ZZ" -ln "LeftIndexFinger_ZZ" -at "double" 
		-p "LeftIndexFinger_Z";
	addAttr -ci true -k true -sn "LeftMiddleFinger_Z" -ln "LeftMiddleFinger_Z" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftMiddleFinger_ZX" -ln "LeftMiddleFinger_ZX" -at "double" 
		-p "LeftMiddleFinger_Z";
	addAttr -ci true -k true -sn "LeftMiddleFinger_ZY" -ln "LeftMiddleFinger_ZY" -at "double" 
		-p "LeftMiddleFinger_Z";
	addAttr -ci true -k true -sn "LeftMiddleFinger_ZZ" -ln "LeftMiddleFinger_ZZ" -at "double" 
		-p "LeftMiddleFinger_Z";
	addAttr -ci true -k true -sn "LeftRingFinger_Z" -ln "LeftRingFinger_Z" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftRingFinger_ZX" -ln "LeftRingFinger_ZX" -at "double" 
		-p "LeftRingFinger_Z";
	addAttr -ci true -k true -sn "LeftRingFinger_ZY" -ln "LeftRingFinger_ZY" -at "double" 
		-p "LeftRingFinger_Z";
	addAttr -ci true -k true -sn "LeftRingFinger_ZZ" -ln "LeftRingFinger_ZZ" -at "double" 
		-p "LeftRingFinger_Z";
	addAttr -ci true -k true -sn "LeftPinkyFinger_Z" -ln "LeftPinkyFinger_Z" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "LeftPinkyFinger_ZX" -ln "LeftPinkyFinger_ZX" -at "double" 
		-p "LeftPinkyFinger_Z";
	addAttr -ci true -k true -sn "LeftPinkyFinger_ZY" -ln "LeftPinkyFinger_ZY" -at "double" 
		-p "LeftPinkyFinger_Z";
	addAttr -ci true -k true -sn "LeftPinkyFinger_ZZ" -ln "LeftPinkyFinger_ZZ" -at "double" 
		-p "LeftPinkyFinger_Z";
	addAttr -ci true -k true -sn "RightThumb_Z" -ln "RightThumb_Z" -at "double3" -nc 
		3;
	addAttr -ci true -k true -sn "RightThumb_ZX" -ln "RightThumb_ZX" -at "double" -p "RightThumb_Z";
	addAttr -ci true -k true -sn "RightThumb_ZY" -ln "RightThumb_ZY" -at "double" -p "RightThumb_Z";
	addAttr -ci true -k true -sn "RightThumb_ZZ" -ln "RightThumb_ZZ" -at "double" -p "RightThumb_Z";
	addAttr -ci true -k true -sn "RightIndexFinger_Z" -ln "RightIndexFinger_Z" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightIndexFinger_ZX" -ln "RightIndexFinger_ZX" -at "double" 
		-p "RightIndexFinger_Z";
	addAttr -ci true -k true -sn "RightIndexFinger_ZY" -ln "RightIndexFinger_ZY" -at "double" 
		-p "RightIndexFinger_Z";
	addAttr -ci true -k true -sn "RightIndexFinger_ZZ" -ln "RightIndexFinger_ZZ" -at "double" 
		-p "RightIndexFinger_Z";
	addAttr -ci true -k true -sn "RightMiddleFinger_Z" -ln "RightMiddleFinger_Z" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightMiddleFinger_ZX" -ln "RightMiddleFinger_ZX" -at "double" 
		-p "RightMiddleFinger_Z";
	addAttr -ci true -k true -sn "RightMiddleFinger_ZY" -ln "RightMiddleFinger_ZY" -at "double" 
		-p "RightMiddleFinger_Z";
	addAttr -ci true -k true -sn "RightMiddleFinger_ZZ" -ln "RightMiddleFinger_ZZ" -at "double" 
		-p "RightMiddleFinger_Z";
	addAttr -ci true -k true -sn "RightRingFinger_Z" -ln "RightRingFinger_Z" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightRingFinger_ZX" -ln "RightRingFinger_ZX" -at "double" 
		-p "RightRingFinger_Z";
	addAttr -ci true -k true -sn "RightRingFinger_ZY" -ln "RightRingFinger_ZY" -at "double" 
		-p "RightRingFinger_Z";
	addAttr -ci true -k true -sn "RightRingFinger_ZZ" -ln "RightRingFinger_ZZ" -at "double" 
		-p "RightRingFinger_Z";
	addAttr -ci true -k true -sn "RightPinkyFinger_Z" -ln "RightPinkyFinger_Z" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "RightPinkyFinger_ZX" -ln "RightPinkyFinger_ZX" -at "double" 
		-p "RightPinkyFinger_Z";
	addAttr -ci true -k true -sn "RightPinkyFinger_ZY" -ln "RightPinkyFinger_ZY" -at "double" 
		-p "RightPinkyFinger_Z";
	addAttr -ci true -k true -sn "RightPinkyFinger_ZZ" -ln "RightPinkyFinger_ZZ" -at "double" 
		-p "RightPinkyFinger_Z";
	addAttr -ci true -k true -sn "Hip" -ln "Hip" -at "double3" -nc 3;
	addAttr -ci true -k true -sn "HipX" -ln "HipX" -at "double" -p "Hip";
	addAttr -ci true -k true -sn "HipY" -ln "HipY" -at "double" -p "Hip";
	addAttr -ci true -k true -sn "HipZ" -ln "HipZ" -at "double" -p "Hip";
	addAttr -ci true -sn "hip_pivot" -ln "hip_pivot" -at "double";
	addAttr -ci true -sn "chest_pivot" -ln "chest_pivot" -at "double";
	addAttr -ci true -sn "spine_length" -ln "spine_length" -at "double";
	addAttr -ci true -sn "spine4_length" -ln "spine4_length" -at "double";
	addAttr -ci true -sn "spine3_length" -ln "spine3_length" -at "double";
	addAttr -ci true -sn "spine2_length" -ln "spine2_length" -at "double";
	addAttr -ci true -sn "spine1_length" -ln "spine1_length" -at "double";
	addAttr -ci true -sn "spine0_length" -ln "spine0_length" -at "double";
	addAttr -ci true -k true -sn "hips_pivot_pos" -ln "hips_pivot_pos" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "hips_pivot_posX" -ln "hips_pivot_posX" -at "double" 
		-p "hips_pivot_pos";
	addAttr -ci true -k true -sn "hips_pivot_posY" -ln "hips_pivot_posY" -at "double" 
		-p "hips_pivot_pos";
	addAttr -ci true -k true -sn "hips_pivot_posZ" -ln "hips_pivot_posZ" -at "double" 
		-p "hips_pivot_pos";
	addAttr -ci true -k true -sn "hips_pivot_neg" -ln "hips_pivot_neg" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "hips_pivot_negX" -ln "hips_pivot_negX" -at "double" 
		-p "hips_pivot_neg";
	addAttr -ci true -k true -sn "hips_pivot_negY" -ln "hips_pivot_negY" -at "double" 
		-p "hips_pivot_neg";
	addAttr -ci true -k true -sn "hips_pivot_negZ" -ln "hips_pivot_negZ" -at "double" 
		-p "hips_pivot_neg";
	addAttr -ci true -k true -sn "chest_pivot_pos" -ln "chest_pivot_pos" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "chest_pivot_posX" -ln "chest_pivot_posX" -at "double" 
		-p "chest_pivot_pos";
	addAttr -ci true -k true -sn "chest_pivot_posY" -ln "chest_pivot_posY" -at "double" 
		-p "chest_pivot_pos";
	addAttr -ci true -k true -sn "chest_pivot_posZ" -ln "chest_pivot_posZ" -at "double" 
		-p "chest_pivot_pos";
	addAttr -ci true -k true -sn "chest_pivot_neg" -ln "chest_pivot_neg" -at "double3" 
		-nc 3;
	addAttr -ci true -k true -sn "chest_pivot_negX" -ln "chest_pivot_negX" -at "double" 
		-p "chest_pivot_neg";
	addAttr -ci true -k true -sn "chest_pivot_negY" -ln "chest_pivot_negY" -at "double" 
		-p "chest_pivot_neg";
	addAttr -ci true -k true -sn "chest_pivot_negZ" -ln "chest_pivot_negZ" -at "double" 
		-p "chest_pivot_neg";
	setAttr ".v" no;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr -k on ".Spine" -type "double3" 1.2923881767996956e-09 113.65819034818404 
		0.34797437991752372 ;
	setAttr -k on ".Spine";
	setAttr -k on ".SpineX";
	setAttr -k on ".SpineY";
	setAttr -k on ".SpineZ";
	setAttr -k on ".Neck" -type "double3" -3.598001210048183e-08 134.5526987099966 -2.2281428972273871 ;
	setAttr -k on ".Neck";
	setAttr -k on ".NeckX";
	setAttr -k on ".NeckY";
	setAttr -k on ".NeckZ";
	setAttr -k on ".Head" -type "double3" -3.5980015974135869e-08 145.33374271634227 
		-2.2281428972274022 ;
	setAttr -k on ".Head";
	setAttr -k on ".HeadX";
	setAttr -k on ".HeadY";
	setAttr -k on ".HeadZ";
	setAttr -k on ".Head_Z" -type "double3" 0 0 1 ;
	setAttr -k on ".Head_Z";
	setAttr -k on ".Head_ZX";
	setAttr -k on ".Head_ZY";
	setAttr -k on ".Head_ZZ";
	setAttr -k on ".LeftHip" -type "double3" 5.8000000000000007 81.960456848129425 -0.17332279682156229 ;
	setAttr -k on ".LeftHip";
	setAttr -k on ".LeftHipX";
	setAttr -k on ".LeftHipY";
	setAttr -k on ".LeftHipZ";
	setAttr -k on ".LeftKnee" -type "double3" 7.0851711407290754 42.459407806388661 
		-0.52721458673467458 ;
	setAttr -k on ".LeftKnee";
	setAttr -k on ".LeftKneeX";
	setAttr -k on ".LeftKneeY";
	setAttr -k on ".LeftKneeZ";
	setAttr -k on ".LeftFoot" -type "double3" 7.0371319428073313 5.1675109863271729 
		-0.87973517179472926 ;
	setAttr -k on ".LeftFoot";
	setAttr -k on ".LeftFootX";
	setAttr -k on ".LeftFootY";
	setAttr -k on ".LeftFootZ";
	setAttr -k on ".LeftToe";
	setAttr -k on ".LeftToeX";
	setAttr -k on ".LeftToeY";
	setAttr -k on ".LeftToeZ";
	setAttr -k on ".LeftCollar" -type "double3" 2.2878770841166736 131.34870205167198 
		-1.704569975474554 ;
	setAttr -k on ".LeftCollar";
	setAttr -k on ".LeftCollarX";
	setAttr -k on ".LeftCollarY";
	setAttr -k on ".LeftCollarZ";
	setAttr -k on ".LeftShoulder" -type "double3" 15.530037881233373 129.96877823117663 
		-4.1381930509593348 ;
	setAttr -k on ".LeftShoulder";
	setAttr -k on ".LeftShoulderX";
	setAttr -k on ".LeftShoulderY";
	setAttr -k on ".LeftShoulderZ";
	setAttr -k on ".LeftElbow" -type "double3" 40.082049371097014 129.96886782184717 
		-4.1400795877922336 ;
	setAttr -k on ".LeftElbow";
	setAttr -k on ".LeftElbowX";
	setAttr -k on ".LeftElbowY";
	setAttr -k on ".LeftElbowZ";
	setAttr -k on ".LeftHand" -type "double3" 64.634625436155972 129.92387099773165 
		-4.1390081443602229 ;
	setAttr -k on ".LeftHand";
	setAttr -k on ".LeftHandX";
	setAttr -k on ".LeftHandY";
	setAttr -k on ".LeftHandZ";
	setAttr -k on ".LeftThumb";
	setAttr -k on ".LeftThumbX";
	setAttr -k on ".LeftThumbY";
	setAttr -k on ".LeftThumbZ";
	setAttr -k on ".LeftIndexFinger" -type "double3" 72.880159379330721 129.71274920017004 
		-1.6435643234073138 ;
	setAttr -k on ".LeftIndexFinger";
	setAttr -k on ".LeftIndexFingerX";
	setAttr -k on ".LeftIndexFingerY";
	setAttr -k on ".LeftIndexFingerZ";
	setAttr -k on ".LeftMiddleFinger";
	setAttr -k on ".LeftMiddleFingerX";
	setAttr -k on ".LeftMiddleFingerY";
	setAttr -k on ".LeftMiddleFingerZ";
	setAttr -k on ".LeftRingFinger";
	setAttr -k on ".LeftRingFingerX";
	setAttr -k on ".LeftRingFingerY";
	setAttr -k on ".LeftRingFingerZ";
	setAttr -k on ".LeftPinkyFinger";
	setAttr -k on ".LeftPinkyFingerX";
	setAttr -k on ".LeftPinkyFingerY";
	setAttr -k on ".LeftPinkyFingerZ";
	setAttr -k on ".LeftBigToe";
	setAttr -k on ".LeftBigToeX";
	setAttr -k on ".LeftBigToeY";
	setAttr -k on ".LeftBigToeZ";
	setAttr -k on ".LeftIndexToe";
	setAttr -k on ".LeftIndexToeX";
	setAttr -k on ".LeftIndexToeY";
	setAttr -k on ".LeftIndexToeZ";
	setAttr -k on ".LeftMiddleToe";
	setAttr -k on ".LeftMiddleToeX";
	setAttr -k on ".LeftMiddleToeY";
	setAttr -k on ".LeftMiddleToeZ";
	setAttr -k on ".LeftRingToe";
	setAttr -k on ".LeftRingToeX";
	setAttr -k on ".LeftRingToeY";
	setAttr -k on ".LeftRingToeZ";
	setAttr -k on ".LeftPinkyToe";
	setAttr -k on ".LeftPinkyToeX";
	setAttr -k on ".LeftPinkyToeY";
	setAttr -k on ".LeftPinkyToeZ";
	setAttr -k on ".LeftCollar_Z";
	setAttr -k on ".LeftCollar_ZX";
	setAttr -k on ".LeftCollar_ZY";
	setAttr -k on ".LeftCollar_ZZ";
	setAttr -k on ".LeftHand_Z" -type "double3" 0 0 1 ;
	setAttr -k on ".LeftHand_Z";
	setAttr -k on ".LeftHand_ZX";
	setAttr -k on ".LeftHand_ZY";
	setAttr -k on ".LeftHand_ZZ";
	setAttr -k on ".RightHip" -type "double3" -7.1333994865404335 81.960464477523956 
		-0.17331913113590861 ;
	setAttr -k on ".RightHip";
	setAttr -k on ".RightHipX";
	setAttr -k on ".RightHipY";
	setAttr -k on ".RightHipZ";
	setAttr -k on ".RightKnee" -type "double3" -7.0851694867001829 42.459362030021474 
		-0.5272191464899999 ;
	setAttr -k on ".RightKnee";
	setAttr -k on ".RightKneeX";
	setAttr -k on ".RightKneeY";
	setAttr -k on ".RightKneeZ";
	setAttr -k on ".RightFoot" -type "double3" -7.0371294878410247 5.1675109863271729 
		-0.87973916530592922 ;
	setAttr -k on ".RightFoot";
	setAttr -k on ".RightFootX";
	setAttr -k on ".RightFootY";
	setAttr -k on ".RightFootZ";
	setAttr -k on ".RightToe";
	setAttr -k on ".RightToeX";
	setAttr -k on ".RightToeY";
	setAttr -k on ".RightToeZ";
	setAttr -k on ".RightCollar" -type "double3" -2.2878799425548468 131.34846363309288 
		-1.7045690218002376 ;
	setAttr -k on ".RightCollar";
	setAttr -k on ".RightCollarX";
	setAttr -k on ".RightCollarY";
	setAttr -k on ".RightCollarZ";
	setAttr -k on ".RightShoulder" -type "double3" -15.529999731675941 129.9684636378615 
		-4.13818899784349 ;
	setAttr -k on ".RightShoulder";
	setAttr -k on ".RightShoulderX";
	setAttr -k on ".RightShoulderY";
	setAttr -k on ".RightShoulderZ";
	setAttr -k on ".RightElbow" -type "double3" -40.08209895957669 129.9684636378573 
		-4.1400789979157979 ;
	setAttr -k on ".RightElbow";
	setAttr -k on ".RightElbowX";
	setAttr -k on ".RightElbowY";
	setAttr -k on ".RightElbowZ";
	setAttr -k on ".RightHand" -type "double3" -64.634598730690328 129.92346363979445 
		-4.1390089979173625 ;
	setAttr -k on ".RightHand";
	setAttr -k on ".RightHandX";
	setAttr -k on ".RightHandY";
	setAttr -k on ".RightHandZ";
	setAttr -k on ".RightThumb";
	setAttr -k on ".RightThumbX";
	setAttr -k on ".RightThumbY";
	setAttr -k on ".RightThumbZ";
	setAttr -k on ".RightIndexFinger";
	setAttr -k on ".RightIndexFingerX";
	setAttr -k on ".RightIndexFingerY";
	setAttr -k on ".RightIndexFingerZ";
	setAttr -k on ".RightMiddleFinger";
	setAttr -k on ".RightMiddleFingerX";
	setAttr -k on ".RightMiddleFingerY";
	setAttr -k on ".RightMiddleFingerZ";
	setAttr -k on ".RightRingFinger";
	setAttr -k on ".RightRingFingerX";
	setAttr -k on ".RightRingFingerY";
	setAttr -k on ".RightRingFingerZ";
	setAttr -k on ".RightPinkyFinger";
	setAttr -k on ".RightPinkyFingerX";
	setAttr -k on ".RightPinkyFingerY";
	setAttr -k on ".RightPinkyFingerZ";
	setAttr -k on ".RightBigToe";
	setAttr -k on ".RightBigToeX";
	setAttr -k on ".RightBigToeY";
	setAttr -k on ".RightBigToeZ";
	setAttr -k on ".RightIndexToe";
	setAttr -k on ".RightIndexToeX";
	setAttr -k on ".RightIndexToeY";
	setAttr -k on ".RightIndexToeZ";
	setAttr -k on ".RightMiddleToe";
	setAttr -k on ".RightMiddleToeX";
	setAttr -k on ".RightMiddleToeY";
	setAttr -k on ".RightMiddleToeZ";
	setAttr -k on ".RightRingToe";
	setAttr -k on ".RightRingToeX";
	setAttr -k on ".RightRingToeY";
	setAttr -k on ".RightRingToeZ";
	setAttr -k on ".RightPinkyToe";
	setAttr -k on ".RightPinkyToeX";
	setAttr -k on ".RightPinkyToeY";
	setAttr -k on ".RightPinkyToeZ";
	setAttr -k on ".RightCollar_Z";
	setAttr -k on ".RightCollar_ZX";
	setAttr -k on ".RightCollar_ZY";
	setAttr -k on ".RightCollar_ZZ";
	setAttr -k on ".RightHand_Z" -type "double3" 0 0 1 ;
	setAttr -k on ".RightHand_Z";
	setAttr -k on ".RightHand_ZX";
	setAttr -k on ".RightHand_ZY";
	setAttr -k on ".RightHand_ZZ";
	setAttr -k on ".Spine_Z";
	setAttr -k on ".Spine_ZX";
	setAttr -k on ".Spine_ZY";
	setAttr -k on ".Spine_ZZ";
	setAttr -k on ".Hip_Z" -type "double3" 0 0 1 ;
	setAttr -k on ".Hip_Z";
	setAttr -k on ".Hip_ZX";
	setAttr -k on ".Hip_ZY";
	setAttr -k on ".Hip_ZZ";
	setAttr -k on ".LeftToe_X";
	setAttr -k on ".LeftToe_XX";
	setAttr -k on ".LeftToe_XY";
	setAttr -k on ".LeftToe_XZ";
	setAttr -k on ".LeftToe_Y";
	setAttr -k on ".LeftToe_YX";
	setAttr -k on ".LeftToe_YY";
	setAttr -k on ".LeftToe_YZ";
	setAttr -k on ".RightToe_X";
	setAttr -k on ".RightToe_XX";
	setAttr -k on ".RightToe_XY";
	setAttr -k on ".RightToe_XZ";
	setAttr -k on ".RightToe_Y";
	setAttr -k on ".RightToe_YX";
	setAttr -k on ".RightToe_YY";
	setAttr -k on ".RightToe_YZ";
	setAttr -k on ".thigh_length" 37.6;
	setAttr -k on ".shin_length" 37.6;
	setAttr -k on ".hip_width" 15.100000000000001;
	setAttr -k on ".LeftThumb1";
	setAttr -k on ".LeftThumb1X";
	setAttr -k on ".LeftThumb1Y";
	setAttr -k on ".LeftThumb1Z";
	setAttr -k on ".LeftThumb2";
	setAttr -k on ".LeftThumb2X";
	setAttr -k on ".LeftThumb2Y";
	setAttr -k on ".LeftThumb2Z";
	setAttr -k on ".LeftIndexFinger1" -type "double3" 76.272770406094011 129.70885097048722 
		-1.6435643528762052 ;
	setAttr -k on ".LeftIndexFinger1";
	setAttr -k on ".LeftIndexFinger1X";
	setAttr -k on ".LeftIndexFinger1Y";
	setAttr -k on ".LeftIndexFinger1Z";
	setAttr -k on ".LeftIndexFinger2" -type "double3" 78.791995765056555 129.70884000570004 
		-1.643564350519167 ;
	setAttr -k on ".LeftIndexFinger2";
	setAttr -k on ".LeftIndexFinger2X";
	setAttr -k on ".LeftIndexFinger2Y";
	setAttr -k on ".LeftIndexFinger2Z";
	setAttr -k on ".LeftMiddleFinger1";
	setAttr -k on ".LeftMiddleFinger1X";
	setAttr -k on ".LeftMiddleFinger1Y";
	setAttr -k on ".LeftMiddleFinger1Z";
	setAttr -k on ".LeftMiddleFinger2";
	setAttr -k on ".LeftMiddleFinger2X";
	setAttr -k on ".LeftMiddleFinger2Y";
	setAttr -k on ".LeftMiddleFinger2Z";
	setAttr -k on ".LeftRingFinger1";
	setAttr -k on ".LeftRingFinger1X";
	setAttr -k on ".LeftRingFinger1Y";
	setAttr -k on ".LeftRingFinger1Z";
	setAttr -k on ".LeftRingFinger2";
	setAttr -k on ".LeftRingFinger2X";
	setAttr -k on ".LeftRingFinger2Y";
	setAttr -k on ".LeftRingFinger2Z";
	setAttr -k on ".LeftPinkyFinger1";
	setAttr -k on ".LeftPinkyFinger1X";
	setAttr -k on ".LeftPinkyFinger1Y";
	setAttr -k on ".LeftPinkyFinger1Z";
	setAttr -k on ".LeftPinkyFinger2";
	setAttr -k on ".LeftPinkyFinger2X";
	setAttr -k on ".LeftPinkyFinger2Y";
	setAttr -k on ".LeftPinkyFinger2Z";
	setAttr -k on ".RightThumb1";
	setAttr -k on ".RightThumb1X";
	setAttr -k on ".RightThumb1Y";
	setAttr -k on ".RightThumb1Z";
	setAttr -k on ".RightThumb2";
	setAttr -k on ".RightThumb2X";
	setAttr -k on ".RightThumb2Y";
	setAttr -k on ".RightThumb2Z";
	setAttr -k on ".RightIndexFinger1";
	setAttr -k on ".RightIndexFinger1X";
	setAttr -k on ".RightIndexFinger1Y";
	setAttr -k on ".RightIndexFinger1Z";
	setAttr -k on ".RightIndexFinger2";
	setAttr -k on ".RightIndexFinger2X";
	setAttr -k on ".RightIndexFinger2Y";
	setAttr -k on ".RightIndexFinger2Z";
	setAttr -k on ".RightMiddleFinger1";
	setAttr -k on ".RightMiddleFinger1X";
	setAttr -k on ".RightMiddleFinger1Y";
	setAttr -k on ".RightMiddleFinger1Z";
	setAttr -k on ".RightMiddleFinger2";
	setAttr -k on ".RightMiddleFinger2X";
	setAttr -k on ".RightMiddleFinger2Y";
	setAttr -k on ".RightMiddleFinger2Z";
	setAttr -k on ".RightRingFinger1";
	setAttr -k on ".RightRingFinger1X";
	setAttr -k on ".RightRingFinger1Y";
	setAttr -k on ".RightRingFinger1Z";
	setAttr -k on ".RightRingFinger2";
	setAttr -k on ".RightRingFinger2X";
	setAttr -k on ".RightRingFinger2Y";
	setAttr -k on ".RightRingFinger2Z";
	setAttr -k on ".RightPinkyFinger1";
	setAttr -k on ".RightPinkyFinger1X";
	setAttr -k on ".RightPinkyFinger1Y";
	setAttr -k on ".RightPinkyFinger1Z";
	setAttr -k on ".RightPinkyFinger2";
	setAttr -k on ".RightPinkyFinger2X";
	setAttr -k on ".RightPinkyFinger2Y";
	setAttr -k on ".RightPinkyFinger2Z";
	setAttr -k on ".hip_pivot" -10;
	setAttr -k on ".chest_pivot" 10;
	setAttr -k on ".spine_length" 10;
	setAttr -k on ".spine4_length" 10;
	setAttr -k on ".spine3_length" 7.6099999999999994;
	setAttr -k on ".spine2_length" 6.96;
	setAttr -k on ".spine1_length" 8.129999999999999;
	setAttr -k on ".spine0_length" 6.5900000000000007;
	setAttr -k on ".hips_pivot_pos";
	setAttr -k on ".hips_pivot_posX";
	setAttr -k on ".hips_pivot_posY";
	setAttr -k on ".hips_pivot_posZ";
	setAttr -k on ".hips_pivot_neg";
	setAttr -k on ".hips_pivot_negX";
	setAttr -k on ".hips_pivot_negY";
	setAttr -k on ".hips_pivot_negZ";
	setAttr -k on ".chest_pivot_pos";
	setAttr -k on ".chest_pivot_posX";
	setAttr -k on ".chest_pivot_posY";
	setAttr -k on ".chest_pivot_posZ";
	setAttr -k on ".chest_pivot_neg";
	setAttr -k on ".chest_pivot_negX";
	setAttr -k on ".chest_pivot_negY";
	setAttr -k on ".chest_pivot_negZ";
createNode nurbsCurve -n "clipShape1" -p "clip";
	rename -uid "C20694B1-4502-6E01-51A6-179FB97DE819";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "clipShape2" -p "clip";
	rename -uid "3B3F0A00-44DE-F38F-7D58-56A4508ED826";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "clipShape3" -p "clip";
	rename -uid "DD26455B-46F4-78DB-5DFB-1B903DE1E37A";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "clipShape4" -p "clip";
	rename -uid "A655DD6F-4C84-C0E3-E2A0-EB815AF23F38";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "clipShape5" -p "clip";
	rename -uid "CF764144-4586-9CA3-5797-A1B8DD216650";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode transform -n "constraints" -p "retarget";
	rename -uid "871A4B70-48E3-D670-6DE9-E69835066B1B";
	setAttr -l on -k off ".v" no;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "RightPinkyFingerShape" -p "retarget";
	rename -uid "48C51C97-4A49-A199-8829-1AAFB905F230";
	setAttr -k off ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -s 4 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "RightRingFingerShape" -p "retarget";
	rename -uid "59A73572-4496-6105-AAD7-08BB649B0FF6";
	setAttr -k off ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -s 4 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "RightMiddleFingerShape" -p "retarget";
	rename -uid "8B029B6F-4CE3-66A9-BF8B-95AB99CADAA0";
	setAttr -k off ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -s 4 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "RightIndexFingerShape" -p "retarget";
	rename -uid "CD20090E-4F5F-1DB9-1C04-D3BD90B4122C";
	setAttr -k off ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -s 4 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "RightThumbShape" -p "retarget";
	rename -uid "636EC112-421D-1DA9-3FCD-E5A6FF7D28E8";
	setAttr -k off ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -s 4 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "LeftPinkyFingerShape" -p "retarget";
	rename -uid "81A814CF-4592-207B-82FF-F995B43EAB57";
	setAttr -k off ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -s 4 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "LeftRingFingerShape" -p "retarget";
	rename -uid "D4B32DC2-4869-B978-0E50-E6B28AB4CCB1";
	setAttr -k off ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -s 4 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "LeftMiddleFingerShape" -p "retarget";
	rename -uid "A7730FF4-4DF6-EB2C-03C7-72AAE9F2ED1E";
	setAttr -k off ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -s 4 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "LeftIndexFingerShape" -p "retarget";
	rename -uid "EF585FE6-459C-02F2-0488-F5822570CFDF";
	setAttr -k off ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -s 4 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		71.345910713888358 126.98207991999745 -1.6089645586533483
		74.667101631468228 126.97826375453813 -1.6089645875018705
		77.133293103322771 126.97825302057797 -1.6089645851944518
		77.133293103322771 126.97825302057797 -1.6089645851944518
		;
createNode nurbsCurve -n "LeftThumbShape" -p "retarget";
	rename -uid "272CE0DB-412F-58BE-DF0E-63B7F56150BB";
	setAttr -k off ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -s 4 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		0 0 0
		0 0 0
		0 0 0
		0 0 0
		;
createNode nurbsCurve -n "LeftCollarShape" -p "retarget";
	rename -uid "59155DA6-49C9-84E8-095C-EDAA9A89EB44";
	setAttr -k off ".v";
	setAttr -s 2 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		2.2397134632780826 128.58359324089847 -1.6686859401994245
		15.203104733769521 127.23271911373581 -4.0510771991301491
		;
createNode nurbsCurve -n "RightCollarShape" -p "retarget";
	rename -uid "794D0E31-41FD-E156-4631-BD9AD1A07111";
	setAttr -k off ".v";
	setAttr -s 2 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		-2.2397162615413744 128.58335984142732 -1.66868500660154
		-15.203067387323776 127.23241114313362 -4.0510732313391395
		;
createNode nurbsCurve -n "LeftArmShape" -p "retarget";
	rename -uid "E7C30D7F-4444-C7BE-9914-348B8B192D69";
	setAttr -k off ".v";
	setAttr -s 3 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 2 0 no 3
		3 0 1 2
		3
		15.203104733769521 127.23271911373581 -4.0510771991301491
		39.238255514449094 127.23280681837362 -4.0529240212225366
		63.273958985076376 127.18875725230386 -4.0518751334582088
		;
createNode nurbsCurve -n "RightArmShape" -p "retarget";
	rename -uid "696C3005-420A-619D-2B33-2FB06002646F";
	setAttr -k off ".v";
	setAttr -s 3 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 2 0 no 3
		3 0 1 2
		3
		-15.203067387323776 127.23241114313362 -4.0510732313391395
		-39.238304059008733 127.23241114312951 -4.0529234437639818
		-63.273932841805234 127.18835846992928 -4.0518759690465496
		;
createNode nurbsCurve -n "SpineShape" -p "retarget";
	rename -uid "61652BC4-4D7A-8278-8A3E-76853691BC3C";
	setAttr -k off ".v";
	setAttr -s 6 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 5 0 no 3
		6 0 1 2 3 4 5
		6
		-0.65266460393909709 80.235056541020583 -0.16967226919071371
		-0.61363326231961146 86.824940275885439 -0.17265812501962047
		-0.49014721418400076 94.95371981706252 -0.24043988404668243
		-0.3596525900885551 101.91000026733111 -0.42680900781231679
		-0.23637850603924293 109.50743007129384 -0.84628948895610745
		-0.16629944591526979 119.46018476411624 -1.8146711026983711
		;
	setAttr ".dcv" yes;
createNode transform -n "Lf_leg_fk1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_leg_fk2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_leg_fk3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "fk_ik" -ln "fk_ik" -min 0 -max 0 -at "double";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
	setAttr -k on ".fk_ik";
createNode transform -n "Lf_leg_pv_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate";
createNode transform -n "Lf_leg_ik_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_index_1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_index_2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_index_3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_mid_1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_mid_2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_mid_3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_ring_1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_ring_2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_ring_3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_pinky_1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_pinky_2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_pinky_3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_thumb_1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_thumb_2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_finger_thumb_3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_index_1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_index_2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_index_3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_mid_1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_mid_2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_mid_3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_ring_1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_ring_2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_ring_3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_pinky_1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_pinky_2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_pinky_3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_thumb_1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_thumb_2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_finger_thumb_3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "spine_hips_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_arm_fk1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_arm_fk2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_arm_fk3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "fk_ik" -ln "fk_ik" -min 0 -max 0 -at "double";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
	setAttr -k on ".fk_ik";
createNode transform -n "Lf_arm_pv_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate";
createNode transform -n "Lf_arm_ik_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_arm_fk1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_arm_fk2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_arm_fk3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "fk_ik" -ln "fk_ik" -min 0 -max 0 -at "double";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
	setAttr -k on ".fk_ik";
createNode transform -n "Rt_arm_pv_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate";
createNode transform -n "Rt_arm_ik_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_leg_fk1_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_leg_fk2_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_leg_fk3_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "fk_ik" -ln "fk_ik" -min 0 -max 0 -at "double";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
	setAttr -k on ".fk_ik";
createNode transform -n "Rt_leg_pv_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate";
createNode transform -n "Rt_leg_ik_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "spine_chest_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Rt_arm_clav_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "Lf_arm_clav_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "root_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate" yes;
	setAttr -k on ".constrain_rotate" yes;
createNode transform -n "head_ctrl" -p "retarget";
	rename -uid "1CF36872-4F3D-7A80-7956-859EFC4FBD70";
	addAttr -ci true -sn "constrain_translate" -ln "constrain_translate" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "constrain_rotate" -ln "constrain_rotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "neck_auto" -ln "neck_auto" -dv 1 -min 0 -max 1 -at "double";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".dla" yes;
	setAttr -k on ".constrain_translate";
	setAttr -k on ".constrain_rotate" yes;
	setAttr -k on ".neck_auto";
createNode pointMatrixMult -n "RightPinkyFinger1";
	rename -uid "955CE151-4FDF-5C31-F97D-7A9AB4334ACC";
createNode fourByFourMatrix -n "Rt_finger_pinky_1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Rt_finger_mid_1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "Center_Head_Z_Vector";
	rename -uid "0C7452D5-40E6-1C4D-26C5-FEA16DFCE11F";
createNode place2dTexture -n "place2dTexture2";
	rename -uid "79A7698C-4D90-9A58-40A9-82AF0641CCBF";
createNode fourByFourMatrix -n "spine_hips_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Rt_finger_thumb_2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "Spine_Z";
	rename -uid "0CCDCE12-4344-1E02-5E2D-98A3AFC333D0";
createNode fourByFourMatrix -n "Rt_finger_mid_2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode expression -n "solver";
	rename -uid "C6E05C05-4A45-FCE5-6558-0491ADE9FCF6";
	setAttr -k on ".nds";
	setAttr -s 247 ".in[236:246]"  0 0 0 0 37.6 37.6 15.100000000000001 0.001 
		0 0 1;
	setAttr -s 236 ".in";
	setAttr -s 678 ".out";
	setAttr ".ixp" -type "string" (
		"vector $Spine = <<.I[0], .I[1], .I[2]>>;\nvector $Neck = <<.I[3], .I[4], .I[5]>>;\nvector $Head = <<.I[6], .I[7], .I[8]>>;\nvector $Head_Z = <<.I[9], .I[10], .I[11]>>;\nvector $Spine_Z = <<.I[12], .I[13], .I[14]>>;\nvector $Hip_Z = <<.I[15], .I[16], .I[17]>>;\nvector $LeftHip = <<.I[18], .I[19], .I[20]>>;\nvector $LeftKnee = <<.I[21], .I[22], .I[23]>>;\nvector $LeftFoot = <<.I[24], .I[25], .I[26]>>;\nvector $LeftToe = <<.I[27], .I[28], .I[29]>>;\nvector $LeftCollar = <<.I[30], .I[31], .I[32]>>;\nvector $LeftShoulder = <<.I[33], .I[34], .I[35]>>;\nvector $LeftElbow = <<.I[36], .I[37], .I[38]>>;\nvector $LeftHand = <<.I[39], .I[40], .I[41]>>;\nvector $LeftBigToe = <<.I[42], .I[43], .I[44]>>;\nvector $LeftIndexToe = <<.I[45], .I[46], .I[47]>>;\nvector $LeftMiddleToe = <<.I[48], .I[49], .I[50]>>;\nvector $LeftRingToe = <<.I[51], .I[52], .I[53]>>;\nvector $LeftPinkyToe = <<.I[54], .I[55], .I[56]>>;\nvector $LeftCollar_Z = <<.I[57], .I[58], .I[59]>>;\nvector $LeftHand_Z = <<.I[60], .I[61], .I[62]>>;\nvector $LeftToe_X = <<.I[63], .I[64], .I[65]>>;\n"
		+ "vector $LeftToe_Y = <<.I[66], .I[67], .I[68]>>;\nvector $LeftThumb = <<.I[69], .I[70], .I[71]>>;\nvector $LeftThumb1 = <<.I[72], .I[73], .I[74]>>;\nvector $LeftThumb2 = <<.I[75], .I[76], .I[77]>>;\nvector $LeftIndexFinger = <<.I[78], .I[79], .I[80]>>;\nvector $LeftIndexFinger1 = <<.I[81], .I[82], .I[83]>>;\nvector $LeftIndexFinger2 = <<.I[84], .I[85], .I[86]>>;\nvector $LeftMiddleFinger = <<.I[87], .I[88], .I[89]>>;\nvector $LeftMiddleFinger1 = <<.I[90], .I[91], .I[92]>>;\nvector $LeftMiddleFinger2 = <<.I[93], .I[94], .I[95]>>;\nvector $LeftRingFinger = <<.I[96], .I[97], .I[98]>>;\nvector $LeftRingFinger1 = <<.I[99], .I[100], .I[101]>>;\nvector $LeftRingFinger2 = <<.I[102], .I[103], .I[104]>>;\nvector $LeftPinkyFinger = <<.I[105], .I[106], .I[107]>>;\nvector $LeftPinkyFinger1 = <<.I[108], .I[109], .I[110]>>;\nvector $LeftPinkyFinger2 = <<.I[111], .I[112], .I[113]>>;\nvector $RightHip = <<.I[114], .I[115], .I[116]>>;\nvector $RightKnee = <<.I[117], .I[118], .I[119]>>;\nvector $RightFoot = <<.I[120], .I[121], .I[122]>>;\nvector $RightToe = <<.I[123], .I[124], .I[125]>>;\n"
		+ "vector $RightCollar = <<.I[126], .I[127], .I[128]>>;\nvector $RightShoulder = <<.I[129], .I[130], .I[131]>>;\nvector $RightElbow = <<.I[132], .I[133], .I[134]>>;\nvector $RightHand = <<.I[135], .I[136], .I[137]>>;\nvector $RightBigToe = <<.I[138], .I[139], .I[140]>>;\nvector $RightIndexToe = <<.I[141], .I[142], .I[143]>>;\nvector $RightMiddleToe = <<.I[144], .I[145], .I[146]>>;\nvector $RightRingToe = <<.I[147], .I[148], .I[149]>>;\nvector $RightPinkyToe = <<.I[150], .I[151], .I[152]>>;\nvector $RightCollar_Z = <<.I[153], .I[154], .I[155]>>;\nvector $RightHand_Z = <<.I[156], .I[157], .I[158]>>;\nvector $RightToe_X = <<.I[159], .I[160], .I[161]>>;\nvector $RightToe_Y = <<.I[162], .I[163], .I[164]>>;\nvector $RightThumb = <<.I[165], .I[166], .I[167]>>;\nvector $RightThumb1 = <<.I[168], .I[169], .I[170]>>;\nvector $RightThumb2 = <<.I[171], .I[172], .I[173]>>;\nvector $RightIndexFinger = <<.I[174], .I[175], .I[176]>>;\nvector $RightIndexFinger1 = <<.I[177], .I[178], .I[179]>>;\nvector $RightIndexFinger2 = <<.I[180], .I[181], .I[182]>>;\n"
		+ "vector $RightMiddleFinger = <<.I[183], .I[184], .I[185]>>;\nvector $RightMiddleFinger1 = <<.I[186], .I[187], .I[188]>>;\nvector $RightMiddleFinger2 = <<.I[189], .I[190], .I[191]>>;\nvector $RightRingFinger = <<.I[192], .I[193], .I[194]>>;\nvector $RightRingFinger1 = <<.I[195], .I[196], .I[197]>>;\nvector $RightRingFinger2 = <<.I[198], .I[199], .I[200]>>;\nvector $RightPinkyFinger = <<.I[201], .I[202], .I[203]>>;\nvector $RightPinkyFinger1 = <<.I[204], .I[205], .I[206]>>;\nvector $RightPinkyFinger2 = <<.I[207], .I[208], .I[209]>>;\nvector $chest_pivot_neg = <<.I[210], .I[211], .I[212]>> * -1;\nvector $chest_pivot_pos = <<.I[213], .I[214], .I[215]>> + $chest_pivot_neg;\nvector $hips_pivot_neg = <<.I[216], .I[217], .I[218]>> * -1;\nvector $hips_pivot_pos = <<.I[219], .I[220], .I[221]>> + $hips_pivot_neg;\n\nfloat $thighLength = .I[222];\nfloat $shinLength = .I[223];\nfloat $hipWidth = .I[224];\n\nfloat $total = $thighLength + $shinLength;\nfloat $inLength = mag($LeftKnee - $LeftHip) + mag($LeftFoot - $LeftKnee);\n$scale = $total/$inLength;\n"
		+ "\n$Spine = $Spine*$scale;\n$Neck = $Neck*$scale;\n$Head = $Head*$scale;\n$Head_Z = $Head_Z*$scale;\n$Spine_Z = $Spine_Z*$scale;\n$Hip_Z = $Hip_Z*$scale;\n$LeftHip = $LeftHip*$scale;\n$LeftKnee = $LeftKnee*$scale;\n$LeftFoot = $LeftFoot*$scale;\n$LeftToe = $LeftToe*$scale;\n$LeftCollar = $LeftCollar*$scale;\n$LeftShoulder = $LeftShoulder*$scale;\n$LeftElbow = $LeftElbow*$scale;\n$LeftHand = $LeftHand*$scale;\n$LeftBigToe = $LeftBigToe*$scale;\n$LeftIndexToe = $LeftIndexToe*$scale;\n$LeftMiddleToe = $LeftMiddleToe*$scale;\n$LeftRingToe = $LeftRingToe*$scale;\n$LeftPinkyToe = $LeftPinkyToe*$scale;\n$LeftCollar_Z = $LeftCollar_Z*$scale;\n$LeftHand_Z = $LeftHand_Z*$scale;\n$LeftToe_X = $LeftToe_X*$scale;\n$LeftToe_Y = $LeftToe_Y*$scale;\n$LeftThumb = $LeftThumb*$scale;\n$LeftThumb1 = $LeftThumb1*$scale;\n$LeftThumb2 = $LeftThumb2*$scale;\n$LeftIndexFinger = $LeftIndexFinger*$scale;\n$LeftIndexFinger1 = $LeftIndexFinger1*$scale;\n$LeftIndexFinger2 = $LeftIndexFinger2*$scale;\n$LeftMiddleFinger = $LeftMiddleFinger*$scale;\n$LeftMiddleFinger1 = $LeftMiddleFinger1*$scale;\n"
		+ "$LeftMiddleFinger2 = $LeftMiddleFinger2*$scale;\n$LeftRingFinger = $LeftRingFinger*$scale;\n$LeftRingFinger1 = $LeftRingFinger1*$scale;\n$LeftRingFinger2 = $LeftRingFinger2*$scale;\n$LeftPinkyFinger = $LeftPinkyFinger*$scale;\n$LeftPinkyFinger1 = $LeftPinkyFinger1*$scale;\n$LeftPinkyFinger2 = $LeftPinkyFinger2*$scale;\n$RightHip = $RightHip*$scale;\n$RightKnee = $RightKnee*$scale;\n$RightFoot = $RightFoot*$scale;\n$RightToe = $RightToe*$scale;\n$RightCollar = $RightCollar*$scale;\n$RightShoulder = $RightShoulder*$scale;\n$RightElbow = $RightElbow*$scale;\n$RightHand = $RightHand*$scale;\n$RightBigToe = $RightBigToe*$scale;\n$RightIndexToe = $RightIndexToe*$scale;\n$RightMiddleToe = $RightMiddleToe*$scale;\n$RightRingToe = $RightRingToe*$scale;\n$RightPinkyToe = $RightPinkyToe*$scale;\n$RightCollar_Z = $RightCollar_Z*$scale;\n$RightHand_Z = $RightHand_Z*$scale;\n$RightToe_X = $RightToe_X*$scale;\n$RightToe_Y = $RightToe_Y*$scale;\n$RightThumb = $RightThumb*$scale;\n$RightThumb1 = $RightThumb1*$scale;\n$RightThumb2 = $RightThumb2*$scale;\n"
		+ "$RightIndexFinger = $RightIndexFinger*$scale;\n$RightIndexFinger1 = $RightIndexFinger1*$scale;\n$RightIndexFinger2 = $RightIndexFinger2*$scale;\n$RightMiddleFinger = $RightMiddleFinger*$scale;\n$RightMiddleFinger1 = $RightMiddleFinger1*$scale;\n$RightMiddleFinger2 = $RightMiddleFinger2*$scale;\n$RightRingFinger = $RightRingFinger*$scale;\n$RightRingFinger1 = $RightRingFinger1*$scale;\n$RightRingFinger2 = $RightRingFinger2*$scale;\n$RightPinkyFinger = $RightPinkyFinger*$scale;\n$RightPinkyFinger1 = $RightPinkyFinger1*$scale;\n$RightPinkyFinger2 = $RightPinkyFinger2*$scale;\n.O[0] = $LeftThumb.x;\n.O[1] = $LeftThumb.y;\n.O[2] = $LeftThumb.z;\n.O[3] = $LeftThumb1.x;\n.O[4] = $LeftThumb1.y;\n.O[5] = $LeftThumb1.z;\n.O[6] = $LeftThumb2.x;\n.O[7] = $LeftThumb2.y;\n.O[8] = $LeftThumb2.z;\n.O[9] = $LeftThumb2.x;\n.O[10] = $LeftThumb2.y;\n.O[11] = $LeftThumb2.z;\n.O[12] = $LeftIndexFinger.x;\n.O[13] = $LeftIndexFinger.y;\n.O[14] = $LeftIndexFinger.z;\n.O[15] = $LeftIndexFinger1.x;\n.O[16] = $LeftIndexFinger1.y;\n.O[17] = $LeftIndexFinger1.z;\n.O[18] = $LeftIndexFinger2.x;\n"
		+ ".O[19] = $LeftIndexFinger2.y;\n.O[20] = $LeftIndexFinger2.z;\n.O[21] = $LeftIndexFinger2.x;\n.O[22] = $LeftIndexFinger2.y;\n.O[23] = $LeftIndexFinger2.z;\n.O[24] = $LeftMiddleFinger.x;\n.O[25] = $LeftMiddleFinger.y;\n.O[26] = $LeftMiddleFinger.z;\n.O[27] = $LeftMiddleFinger1.x;\n.O[28] = $LeftMiddleFinger1.y;\n.O[29] = $LeftMiddleFinger1.z;\n.O[30] = $LeftMiddleFinger2.x;\n.O[31] = $LeftMiddleFinger2.y;\n.O[32] = $LeftMiddleFinger2.z;\n.O[33] = $LeftMiddleFinger2.x;\n.O[34] = $LeftMiddleFinger2.y;\n.O[35] = $LeftMiddleFinger2.z;\n.O[36] = $LeftRingFinger.x;\n.O[37] = $LeftRingFinger.y;\n.O[38] = $LeftRingFinger.z;\n.O[39] = $LeftRingFinger1.x;\n.O[40] = $LeftRingFinger1.y;\n.O[41] = $LeftRingFinger1.z;\n.O[42] = $LeftRingFinger2.x;\n.O[43] = $LeftRingFinger2.y;\n.O[44] = $LeftRingFinger2.z;\n.O[45] = $LeftRingFinger2.x;\n.O[46] = $LeftRingFinger2.y;\n.O[47] = $LeftRingFinger2.z;\n.O[48] = $LeftPinkyFinger.x;\n.O[49] = $LeftPinkyFinger.y;\n.O[50] = $LeftPinkyFinger.z;\n.O[51] = $LeftPinkyFinger1.x;\n.O[52] = $LeftPinkyFinger1.y;\n.O[53] = $LeftPinkyFinger1.z;\n"
		+ ".O[54] = $LeftPinkyFinger2.x;\n.O[55] = $LeftPinkyFinger2.y;\n.O[56] = $LeftPinkyFinger2.z;\n.O[57] = $LeftPinkyFinger2.x;\n.O[58] = $LeftPinkyFinger2.y;\n.O[59] = $LeftPinkyFinger2.z;\n.O[60] = $LeftCollar.x;\n.O[61] = $LeftCollar.y;\n.O[62] = $LeftCollar.z;\nif ($LeftCollar.y == 0){\n.O[63] = 0;\n.O[64] = 0;\n.O[65] = 0;\n}else{\n.O[63] = $LeftShoulder.x;\n.O[64] = $LeftShoulder.y;\n.O[65] = $LeftShoulder.z;\n}\n.O[66] = $LeftShoulder.x;\n.O[67] = $LeftShoulder.y;\n.O[68] = $LeftShoulder.z;\n.O[69] = $LeftElbow.x;\n.O[70] = $LeftElbow.y;\n.O[71] = $LeftElbow.z;\n.O[72] = $LeftHand.x;\n.O[73] = $LeftHand.y;\n.O[74] = $LeftHand.z;\n.O[75] = $RightThumb.x;\n.O[76] = $RightThumb.y;\n.O[77] = $RightThumb.z;\n.O[78] = $RightThumb1.x;\n.O[79] = $RightThumb1.y;\n.O[80] = $RightThumb1.z;\n.O[81] = $RightThumb2.x;\n.O[82] = $RightThumb2.y;\n.O[83] = $RightThumb2.z;\n.O[84] = $RightThumb2.x;\n.O[85] = $RightThumb2.y;\n.O[86] = $RightThumb2.z;\n.O[87] = $RightIndexFinger.x;\n.O[88] = $RightIndexFinger.y;\n.O[89] = $RightIndexFinger.z;\n.O[90] = $RightIndexFinger1.x;\n"
		+ ".O[91] = $RightIndexFinger1.y;\n.O[92] = $RightIndexFinger1.z;\n.O[93] = $RightIndexFinger2.x;\n.O[94] = $RightIndexFinger2.y;\n.O[95] = $RightIndexFinger2.z;\n.O[96] = $RightIndexFinger2.x;\n.O[97] = $RightIndexFinger2.y;\n.O[98] = $RightIndexFinger2.z;\n.O[99] = $RightMiddleFinger.x;\n.O[100] = $RightMiddleFinger.y;\n.O[101] = $RightMiddleFinger.z;\n.O[102] = $RightMiddleFinger1.x;\n.O[103] = $RightMiddleFinger1.y;\n.O[104] = $RightMiddleFinger1.z;\n.O[105] = $RightMiddleFinger2.x;\n.O[106] = $RightMiddleFinger2.y;\n.O[107] = $RightMiddleFinger2.z;\n.O[108] = $RightMiddleFinger2.x;\n.O[109] = $RightMiddleFinger2.y;\n.O[110] = $RightMiddleFinger2.z;\n.O[111] = $RightRingFinger.x;\n.O[112] = $RightRingFinger.y;\n.O[113] = $RightRingFinger.z;\n.O[114] = $RightRingFinger1.x;\n.O[115] = $RightRingFinger1.y;\n.O[116] = $RightRingFinger1.z;\n.O[117] = $RightRingFinger2.x;\n.O[118] = $RightRingFinger2.y;\n.O[119] = $RightRingFinger2.z;\n.O[120] = $RightRingFinger2.x;\n.O[121] = $RightRingFinger2.y;\n.O[122] = $RightRingFinger2.z;\n.O[123] = $RightPinkyFinger.x;\n"
		+ ".O[124] = $RightPinkyFinger.y;\n.O[125] = $RightPinkyFinger.z;\n.O[126] = $RightPinkyFinger1.x;\n.O[127] = $RightPinkyFinger1.y;\n.O[128] = $RightPinkyFinger1.z;\n.O[129] = $RightPinkyFinger2.x;\n.O[130] = $RightPinkyFinger2.y;\n.O[131] = $RightPinkyFinger2.z;\n.O[132] = $RightPinkyFinger2.x;\n.O[133] = $RightPinkyFinger2.y;\n.O[134] = $RightPinkyFinger2.z;\n.O[135] = $RightCollar.x;\n.O[136] = $RightCollar.y;\n.O[137] = $RightCollar.z;\nif ($LeftCollar.y == 0){\n.O[138] = 0;\n.O[139] = 0;\n.O[140] = 0;\n}else{\n.O[138] = $RightShoulder.x;\n.O[139] = $RightShoulder.y;\n.O[140] = $RightShoulder.z;\n}\n.O[141] = $RightShoulder.x;\n.O[142] = $RightShoulder.y;\n.O[143] = $RightShoulder.z;\n.O[144] = $RightElbow.x;\n.O[145] = $RightElbow.y;\n.O[146] = $RightElbow.z;\n.O[147] = $RightHand.x;\n.O[148] = $RightHand.y;\n.O[149] = $RightHand.z;\n\nvector $left_prev = <<.O[150], .O[151], .O[152]>> * $scale;\nvector $right_prev = <<.O[153], .O[154], .O[155]>> * $scale;\n\n//need to get root position and orientation, and then project hip width to get the ik targets.\n"
		+ "//HIP INITIAL\nvector $cv0 = ($LeftHip+$RightHip)/2;\nvector $hip_x = unit($LeftHip-$RightHip);\nvector $hip_offset = $hip_x*$hipWidth*0.5;\nvector $Lf_hip_ee = $cv0+$hip_offset;\nvector $Rt_hip_ee = $cv0-$hip_offset;\n\n//CHEST ORIENTATION\nvector $chest_x = unit($LeftShoulder - $RightShoulder);\nif ($LeftCollar.y != 0){\n    $chest_x = unit($LeftCollar - $RightCollar);\n}\nvector $chest_y = unit($Neck - $Spine);\nvector $chest_z = unit(cross($chest_x, $chest_y));\n$chest_y = cross($chest_z,$chest_x);\n\n\n//sort out spine orientation and position, then offset after ik solve\nfloat $spine_length = (.I[225] + .I[226] + .I[227] + .I[228] + .I[229]) * 0.95; //make it slightly shorter, since spines aren't often in line.\nvector $hip_y = unit(cross($Hip_Z, $hip_x));\nvector $cv1 = $cv0 + $hip_y * ($spine_length/3);\nvector $cv3 = unit($Neck-$cv0) * $spine_length + $cv0;\nvector $cv2 = $cv3 - $chest_y * ($spine_length/3);\n\n//lock down feet by tracking the last position, and if it doesn't move very far, keep it at the previous position\n//should be looking at source position for locking.\n"
		+ "\nfloat $tol = $scale * .I[230];\nif (mag($LeftFoot - $left_prev) < $tol){\n    $LeftFoot = $left_prev;\n}else{\n    .O[150] = $LeftFoot.x;\n    .O[151] = $LeftFoot.y;\n    .O[152] = $LeftFoot.z;\n}\nif (mag($RightFoot - $right_prev) < $tol){\n    $RightFoot = $right_prev;\n}else{\n    .O[153] = $RightFoot.x;\n    .O[154] = $RightFoot.y;\n    .O[155] = $RightFoot.z;\n}\n\n//ik solve legs, but solve from foot to hip target.\n$total = $thighLength + $shinLength;\nvector $eeVector = $Lf_hip_ee - $LeftFoot;\nvector $eeUnit = unit($eeVector);\nvector $lperp = cross($eeUnit, $LeftKnee-$LeftFoot);\nfloat $eeDistance = clamp(0.01, $total-0.01, mag($eeVector));\n\n//herons formula\nfloat $s = ($eeDistance + $total) * 0.5;\nfloat $area = sqrt($s * ($s-$eeDistance) * ($s-$thighLength) * ($s-$shinLength));\nfloat $height = ($area * 2)/$eeDistance;\nfloat $b = sqrt($thighLength * $thighLength - $height * $height);\n\nvector $base = $eeUnit * $b;\nvector $heightVector = unit(cross($lperp, $eeVector)) * $height;\nvector $LeftKnee_pnt = $base + $LeftFoot + $heightVector;\n"
		+ "vector $LeftHip_pnt = ($eeUnit * $eeDistance) + $LeftFoot;\n\n$total = $thighLength + $shinLength;\n$eeVector = $Rt_hip_ee - $RightFoot;\n$eeUnit = unit($eeVector);\nvector $rperp = cross($eeUnit, $RightKnee-$RightFoot);\n$eeDistance = clamp(0.01, $total-0.01, mag($eeVector));\n\n//herons formula\n$s = ($eeDistance + $total) * 0.5;\n$area = sqrt($s * ($s-$eeDistance) * ($s-$thighLength) * ($s-$shinLength));\n$height = ($area * 2)/$eeDistance;\n$b = sqrt($thighLength * $thighLength - $height * $height);\n\n$base = $eeUnit * $b;\n$heightVector = unit(cross($rperp, $eeVector)) * $height;\nvector $RightKnee_pnt = $base + $RightFoot + $heightVector;\nvector $RightHip_pnt = ($eeUnit * $eeDistance) + $RightFoot;\n\nvector $root_pnt = ($LeftHip_pnt+$RightHip_pnt)/2;\n\n//get the chest scale\n//check based on new positions\n//just have to scale the chest by the root position, I guess? \n//should be global, ideally.\n//SCALE shoulder and clav \n//we don't care about the fabrik solve anymore?\n\n$Spine = $Spine*$scale;\n$Neck = $Neck*$scale;\n$Head = $Head*$scale;\n"
		+ "$Head_Z = $Head_Z*$scale;\n$Spine_Z = $Spine_Z*$scale;\n$Hip_Z = $Hip_Z*$scale;\n$LeftHip = $LeftHip*$scale;\n$LeftKnee = $LeftKnee*$scale;\n$LeftFoot = $LeftFoot*$scale;\n$LeftToe = $LeftToe*$scale;\n$LeftCollar = $LeftCollar*$scale;\n$LeftShoulder = $LeftShoulder*$scale;\n$LeftElbow = $LeftElbow*$scale;\n$LeftHand = $LeftHand*$scale;\n$LeftBigToe = $LeftBigToe*$scale;\n$LeftIndexToe = $LeftIndexToe*$scale;\n$LeftMiddleToe = $LeftMiddleToe*$scale;\n$LeftRingToe = $LeftRingToe*$scale;\n$LeftPinkyToe = $LeftPinkyToe*$scale;\n$LeftCollar_Z = $LeftCollar_Z*$scale;\n$LeftHand_Z = $LeftHand_Z*$scale;\n$LeftToe_X = $LeftToe_X*$scale;\n$LeftToe_Y = $LeftToe_Y*$scale;\n$LeftThumb = $LeftThumb*$scale;\n$LeftThumb1 = $LeftThumb1*$scale;\n$LeftThumb2 = $LeftThumb2*$scale;\n$LeftIndexFinger = $LeftIndexFinger*$scale;\n$LeftIndexFinger1 = $LeftIndexFinger1*$scale;\n$LeftIndexFinger2 = $LeftIndexFinger2*$scale;\n$LeftMiddleFinger = $LeftMiddleFinger*$scale;\n$LeftMiddleFinger1 = $LeftMiddleFinger1*$scale;\n$LeftMiddleFinger2 = $LeftMiddleFinger2*$scale;\n"
		+ "$LeftRingFinger = $LeftRingFinger*$scale;\n$LeftRingFinger1 = $LeftRingFinger1*$scale;\n$LeftRingFinger2 = $LeftRingFinger2*$scale;\n$LeftPinkyFinger = $LeftPinkyFinger*$scale;\n$LeftPinkyFinger1 = $LeftPinkyFinger1*$scale;\n$LeftPinkyFinger2 = $LeftPinkyFinger2*$scale;\n$RightHip = $RightHip*$scale;\n$RightKnee = $RightKnee*$scale;\n$RightFoot = $RightFoot*$scale;\n$RightToe = $RightToe*$scale;\n$RightCollar = $RightCollar*$scale;\n$RightShoulder = $RightShoulder*$scale;\n$RightElbow = $RightElbow*$scale;\n$RightHand = $RightHand*$scale;\n$RightBigToe = $RightBigToe*$scale;\n$RightIndexToe = $RightIndexToe*$scale;\n$RightMiddleToe = $RightMiddleToe*$scale;\n$RightRingToe = $RightRingToe*$scale;\n$RightPinkyToe = $RightPinkyToe*$scale;\n$RightCollar_Z = $RightCollar_Z*$scale;\n$RightHand_Z = $RightHand_Z*$scale;\n$RightToe_X = $RightToe_X*$scale;\n$RightToe_Y = $RightToe_Y*$scale;\n$RightThumb = $RightThumb*$scale;\n$RightThumb1 = $RightThumb1*$scale;\n$RightThumb2 = $RightThumb2*$scale;\n$RightIndexFinger = $RightIndexFinger*$scale;\n$RightIndexFinger1 = $RightIndexFinger1*$scale;\n"
		+ "$RightIndexFinger2 = $RightIndexFinger2*$scale;\n$RightMiddleFinger = $RightMiddleFinger*$scale;\n$RightMiddleFinger1 = $RightMiddleFinger1*$scale;\n$RightMiddleFinger2 = $RightMiddleFinger2*$scale;\n$RightRingFinger = $RightRingFinger*$scale;\n$RightRingFinger1 = $RightRingFinger1*$scale;\n$RightRingFinger2 = $RightRingFinger2*$scale;\n$RightPinkyFinger = $RightPinkyFinger*$scale;\n$RightPinkyFinger1 = $RightPinkyFinger1*$scale;\n$RightPinkyFinger2 = $RightPinkyFinger2*$scale;\n\n//root matrix\nvector $y = <<0,1,0>>;\nvector $z = unit(cross($hip_x,$y));\nvector $x = cross($y,$z);\n.O[156] = $x.x;\n.O[157] = $x.y;\n.O[158] = $x.z;\n.O[159] = $y.x;\n.O[160] = $y.y;\n.O[161] = $y.z;\n.O[162] = $z.x;\n.O[163] = $z.y;\n.O[164] = $z.z;\n.O[165] = $cv0.x;\n.O[166] = $cv0.y;\n.O[167] = $cv0.z;\n\n//PIVOT TODO\n//need to calculate the offset from the ends of the spine chain to the different pivot positions\n//may need to add that data into the spine module?\n//don't know the default offset?\n//might be able to get current offset from decomposition?\n"
		+ "//actually the controlCurve offset should be what we need?\n\n//hip orientation stays the same, pivot is cv1\nvector $hip_z = cross($hip_x,$hip_y);\n\nvector $pivot_offset = <<0,0,0>>;\nif (.I[231] < 0){\n    $pivot_offset = $hips_pivot_neg * (1-.I[231]*-0.1);\n}else{\n    float $p = .I[231]*0.1;\n    $pivot_offset = $hips_pivot_neg * (1-$p) + $hips_pivot_pos * $p;\n}\n//TODO\n//THis pivot needs to be rotated.\n\nvector $invX = <<$hip_x.x, $hip_y.x, $hip_z.x>>;\nvector $invY = <<$hip_x.y, $hip_y.y, $hip_z.y>>;\nvector $invZ = <<$hip_x.z, $hip_y.z, $hip_z.z>>;\n\n$pivot_offset = <<dot($pivot_offset,$invX), dot($pivot_offset, $invY), dot($pivot_offset, $invZ)>>;\nvector $hip_pnt = $cv0 + $pivot_offset; \n\n.O[168] = $hip_x.x;\n.O[169] = $hip_x.y;\n.O[170] = $hip_x.z;\n.O[171] = $hip_y.x;\n.O[172] = $hip_y.y;\n.O[173] = $hip_y.z;\n.O[174] = $hip_z.x;\n.O[175] = $hip_z.y;\n.O[176] = $hip_z.z;\n.O[177] = $hip_pnt.x;\n.O[178] = $hip_pnt.y;\n.O[179] = $hip_pnt.z;\n\n//sample points on the spine curve:\nfloat $t1 = .I[225]/$spine_length;\nfloat $t2 = .I[226]/$spine_length + $t1;\n"
		+ "float $t3 = .I[227]/$spine_length + $t2;\nfloat $t4 = .I[228]/$spine_length + $t3;\nvector $pnt1 = ($cv0*(1-$t1) + $cv3*$t1)*(1-((1-$t1)*$t1)) +((3*$cv1-$cv0-$cv3)*(1-$t1) + (3*$cv2-$cv3-$cv0)*$t1)*((1-$t1)*$t1);\nvector $pnt2 = ($cv0*(1-$t2) + $cv3*$t2)*(1-((1-$t2)*$t2)) +((3*$cv1-$cv0-$cv3)*(1-$t2) + (3*$cv2-$cv3-$cv0)*$t2)*((1-$t2)*$t2);\nvector $pnt3 = ($cv0*(1-$t3) + $cv3*$t3)*(1-((1-$t3)*$t3)) +((3*$cv1-$cv0-$cv3)*(1-$t3) + (3*$cv2-$cv3-$cv0)*$t3)*((1-$t3)*$t3);\nvector $pnt4 = ($cv0*(1-$t4) + $cv3*$t4)*(1-((1-$t4)*$t4)) +((3*$cv1-$cv0-$cv3)*(1-$t4) + (3*$cv2-$cv3-$cv0)*$t4)*((1-$t4)*$t4);\n\n\n// //do a fabrik solve to maintain the correct distance\n$pnt0 = $cv0;\n$pnt1 = unit($pnt1-$cv0) * .I[225] + $cv0;\n$pnt2 = unit($pnt2-$pnt1) * .I[226] + $pnt1;\n$pnt3 = unit($pnt3-$pnt2) * .I[227] + $pnt2;\n$pnt4 = unit($pnt4-$pnt3) * .I[228] + $pnt3;\nvector $pnt5 = unit($cv3-$pnt4) * .I[229] + $pnt4;\n\n.O[180] = $pnt0.x;\n.O[181] = $pnt0.y;\n.O[182] = $pnt0.z;\n.O[183] = $pnt1.x;\n.O[184] = $pnt1.y;\n.O[185] = $pnt1.z;\n.O[186] = $pnt2.x;\n"
		+ ".O[187] = $pnt2.y;\n.O[188] = $pnt2.z;\n.O[189] = $pnt3.x;\n.O[190] = $pnt3.y;\n.O[191] = $pnt3.z;\n.O[192] = $pnt4.x;\n.O[193] = $pnt4.y;\n.O[194] = $pnt4.z;\n.O[195] = $pnt5.x;\n.O[196] = $pnt5.y;\n.O[197] = $pnt5.z;\n\n//CHEST\n\n$pivot_offset = <<0,0,0>>;\nif (.I[232] > 0){\n    $pivot_offset = $chest_pivot_neg * -1 * (1-.I[232]*0.1);\n}else{\n$p = .I[232]*-0.1;\n    $pivot_offset = $chest_pivot_pos * $p * -1 + $chest_pivot_neg * (1-$p) * -1;\n}\n//TODO\n//THis pivot needs to be rotated.\n\n$invX = <<$chest_x.x, $chest_y.x, $chest_z.x>>;\n$invY = <<$chest_x.y, $chest_y.y, $chest_z.y>>;\n$invZ = <<$chest_x.z, $chest_y.z, $chest_z.z>>;\n\n$pivot_offset = <<dot($pivot_offset,$invX), dot($pivot_offset, $invY), dot($pivot_offset, $invZ)>>;\nvector $chest_pnt = $pnt5 + $pivot_offset; \n\n.O[198] = $chest_x.x;\n.O[199] = $chest_x.y;\n.O[200] = $chest_x.z;\n.O[201] = $chest_y.x;\n.O[202] = $chest_y.y;\n.O[203] = $chest_y.z;\n.O[204] = $chest_z.x;\n.O[205] = $chest_z.y;\n.O[206] = $chest_z.z;\n.O[207] = $chest_pnt.x;\n.O[208] = $chest_pnt.y;\n.O[209] = $chest_pnt.z;\n"
		+ "\n//LEGS\n//Lf\n.O[210] = $LeftHip_pnt.x;\n.O[211] = $LeftHip_pnt.y;\n.O[212] = $LeftHip_pnt.z;\n.O[213] = $LeftKnee_pnt.x;\n.O[214] = $LeftKnee_pnt.y;\n.O[215] = $LeftKnee_pnt.z;\n.O[216] = $LeftFoot.x;\n.O[217] = $LeftFoot.y;\n.O[218] = $LeftFoot.z;\n.O[219] = $RightHip_pnt.x;\n.O[220] = $RightHip_pnt.y;\n.O[221] = $RightHip_pnt.z;\n.O[222] = $RightKnee_pnt.x;\n.O[223] = $RightKnee_pnt.y;\n.O[224] = $RightKnee_pnt.z;\n.O[225] = $RightFoot.x;\n.O[226] = $RightFoot.y;\n.O[227] = $RightFoot.z;\n\n$y = unit($LeftKnee_pnt - $LeftHip_pnt);\n$x = $lperp;\n$z = cross($x, $y);\n.O[228] = $x.x;\n.O[229] = $x.y;\n.O[230] = $x.z;\n.O[231] = $y.x;\n.O[232] = $y.y;\n.O[233] = $y.z;\n.O[234] = $z.x;\n.O[235] = $z.y;\n.O[236] = $z.z;\n.O[237] = $LeftHip_pnt.x;\n.O[238] = $LeftHip_pnt.y;\n.O[239] = $LeftHip_pnt.z;\n\n$y = unit($LeftFoot - $LeftKnee_pnt);\n$z = cross($x, $y);\n.O[240] = $x.x;\n.O[241] = $x.y;\n.O[242] = $x.z;\n.O[243] = $y.x;\n.O[244] = $y.y;\n.O[245] = $y.z;\n.O[246] = $z.x;\n.O[247] = $z.y;\n.O[248] = $z.z;\n.O[249] = $LeftKnee_pnt.x;\n.O[250] = $LeftKnee_pnt.y;\n"
		+ ".O[251] = $LeftKnee_pnt.z;\n\n$z = unit($LeftFoot-$LeftToe);\n$x = unit(cross($z,$y)) * -1;\n$z = rot($z, $x, deg_to_rad(.I[233]));\n$y = cross($z, $x);\n\n.O[252] = $x.x;\n.O[253] = $x.y;\n.O[254] = $x.z;\n.O[255] = $y.x;\n.O[256] = $y.y;\n.O[257] = $y.z;\n.O[258] = $z.x;\n.O[259] = $z.y;\n.O[260] = $z.z;\n.O[261] = $LeftFoot.x;\n.O[262] = $LeftFoot.y;\n.O[263] = $LeftFoot.z;\n$y = $y*-1;\n$z = $z*-1;\n.O[264] = $x.x;\n.O[265] = $x.y;\n.O[266] = $x.z;\n.O[267] = $y.x;\n.O[268] = $y.y;\n.O[269] = $y.z;\n.O[270] = $z.x;\n.O[271] = $z.y;\n.O[272] = $z.z;\n.O[273] = $LeftFoot.x;\n.O[274] = $LeftFoot.y;\n.O[275] = $LeftFoot.z;\n\n//PV\nvector $mid = $LeftHip_pnt * ($shinLength/$total) + $LeftFoot * ($thighLength/$total);\nvector $pv = (unit($LeftKnee_pnt - $mid) * $total * 0.5) + $LeftKnee_pnt;\n.O[276] = $pv.x;\n.O[277] = $pv.y;\n.O[278] = $pv.z;\n\n//Rt\n$y = unit($RightHip_pnt - $RightKnee_pnt);\n$x = $rperp;\n$z = cross($x, $y);\n.O[279] = $x.x;\n.O[280] = $x.y;\n.O[281] = $x.z;\n.O[282] = $y.x;\n.O[283] = $y.y;\n.O[284] = $y.z;\n.O[285] = $z.x;\n.O[286] = $z.y;\n"
		+ ".O[287] = $z.z;\n.O[288] = $RightHip_pnt.x;\n.O[289] = $RightHip_pnt.y;\n.O[290] = $RightHip_pnt.z;\n\n$y = unit($RightKnee_pnt - $RightFoot);\n$z = cross($x, $y);\n.O[291] = $x.x;\n.O[292] = $x.y;\n.O[293] = $x.z;\n.O[294] = $y.x;\n.O[295] = $y.y;\n.O[296] = $y.z;\n.O[297] = $z.x;\n.O[298] = $z.y;\n.O[299] = $z.z;\n.O[300] = $RightKnee_pnt.x;\n.O[301] = $RightKnee_pnt.y;\n.O[302] = $RightKnee_pnt.z;\n\n$z = unit($RightToe-$RightFoot);\n$x = unit(cross($y,$z));\n$z = rot($z, $x, deg_to_rad(.I[233]));\n$y = cross($z, $x);\n\n.O[303] = $x.x;\n.O[304] = $x.y;\n.O[305] = $x.z;\n.O[306] = $y.x;\n.O[307] = $y.y;\n.O[308] = $y.z;\n.O[309] = $z.x;\n.O[310] = $z.y;\n.O[311] = $z.z;\n.O[312] = $RightFoot.x;\n.O[313] = $RightFoot.y;\n.O[314] = $RightFoot.z;\n.O[315] = $x.x;\n.O[316] = $x.y;\n.O[317] = $x.z;\n.O[318] = $y.x;\n.O[319] = $y.y;\n.O[320] = $y.z;\n.O[321] = $z.x;\n.O[322] = $z.y;\n.O[323] = $z.z;\n.O[324] = $RightFoot.x;\n.O[325] = $RightFoot.y;\n.O[326] = $RightFoot.z;\n\n$mid = $RightHip_pnt * ($shinLength/$total) + $RightFoot * ($thighLength/$total);\n$pv = (unit($RightKnee_pnt - $mid) * $total * 0.5) + $RightKnee_pnt;\n"
		+ ".O[327] = $pv.x;\n.O[328] = $pv.y;\n.O[329] = $pv.z;\n\n//HEAD\n$z = $Head_Z;\n$x = unit(cross($Head-$Neck, $z));\n$y = unit(cross($z,$x));\n//#axisOut: head, $x, $y, $z, $Head\n.O[330] = $x.x;\n.O[331] = $x.y;\n.O[332] = $x.z;\n.O[333] = $y.x;\n.O[334] = $y.y;\n.O[335] = $y.z;\n.O[336] = $z.x;\n.O[337] = $z.y;\n.O[338] = $z.z;\n.O[339] = $Head.x;\n.O[340] = $Head.y;\n.O[341] = $Head.z;\n\n//ARMS\n\n//clav\n$x = rot(unit($LeftShoulder - $LeftCollar), $chest_z, .I[234]*0.02);\n$y = unit(cross($chest_z, $x));\n$z = cross($x,$y);\n\n.O[342] = $x.x;\n.O[343] = $x.y;\n.O[344] = $x.z;\n.O[345] = $y.x;\n.O[346] = $y.y;\n.O[347] = $y.z;\n.O[348] = $z.x;\n.O[349] = $z.y;\n.O[350] = $z.z;\n.O[351] = $LeftCollar.x;\n.O[352] = $LeftCollar.y;\n.O[353] = $LeftCollar.z;\n\nvector $upp = unit($LeftElbow - $LeftShoulder);\nvector $low = unit($LeftHand - $LeftElbow);\n$x = unit(cross($low, $upp));\n\n$y = $upp;\n$z = cross($x, $y);\n.O[354] = $x.x;\n.O[355] = $x.y;\n.O[356] = $x.z;\n.O[357] = $y.x;\n.O[358] = $y.y;\n.O[359] = $y.z;\n.O[360] = $z.x;\n.O[361] = $z.y;\n.O[362] = $z.z;\n"
		+ ".O[363] = $LeftShoulder.x;\n.O[364] = $LeftShoulder.y;\n.O[365] = $LeftShoulder.z;\n\n$y = $low;\n$z = cross($x, $y);\n.O[366] = $x.x;\n.O[367] = $x.y;\n.O[368] = $x.z;\n.O[369] = $y.x;\n.O[370] = $y.y;\n.O[371] = $y.z;\n.O[372] = $z.x;\n.O[373] = $z.y;\n.O[374] = $z.z;\n.O[375] = $LeftElbow.x;\n.O[376] = $LeftElbow.y;\n.O[377] = $LeftElbow.z;\n\nif (.I[235] == 0){\n    $z = $LeftHand_Z;\n    $x = unit(cross($low,$z));\n}else{\n    $x = $LeftHand_Z * -1;\n    $z = unit(cross($x,$low));\n}\nvector $Left_hand_z = $z;\n$y = cross($z,$x);\n.O[378] = $x.x;\n.O[379] = $x.y;\n.O[380] = $x.z;\n.O[381] = $y.x;\n.O[382] = $y.y;\n.O[383] = $y.z;\n.O[384] = $z.x;\n.O[385] = $z.y;\n.O[386] = $z.z;\n.O[387] = $LeftHand.x;\n.O[388] = $LeftHand.y;\n.O[389] = $LeftHand.z;\n\n\n//clav\n$x = rot(unit($RightCollar-$RightShoulder), $chest_z, .I[234]*-0.02);\n$y = unit(cross($chest_z, $x)*-1);\n$z = cross($x,$y);\n\n.O[390] = $x.x;\n.O[391] = $x.y;\n.O[392] = $x.z;\n.O[393] = $y.x;\n.O[394] = $y.y;\n.O[395] = $y.z;\n.O[396] = $z.x;\n.O[397] = $z.y;\n.O[398] = $z.z;\n.O[399] = $RightCollar.x;\n"
		+ ".O[400] = $RightCollar.y;\n.O[401] = $RightCollar.z;\n\n$upp = unit($RightShoulder - $RightElbow);\n$low = unit($RightElbow - $RightHand);\n$x = unit(cross($low, $upp));\n\n$y = $upp;\n$z = cross($x, $y);\n.O[402] = $x.x;\n.O[403] = $x.y;\n.O[404] = $x.z;\n.O[405] = $y.x;\n.O[406] = $y.y;\n.O[407] = $y.z;\n.O[408] = $z.x;\n.O[409] = $z.y;\n.O[410] = $z.z;\n.O[411] = $RightShoulder.x;\n.O[412] = $RightShoulder.y;\n.O[413] = $RightShoulder.z;\n\n$y = $low;\n$z = cross($x, $y);\n.O[414] = $x.x;\n.O[415] = $x.y;\n.O[416] = $x.z;\n.O[417] = $y.x;\n.O[418] = $y.y;\n.O[419] = $y.z;\n.O[420] = $z.x;\n.O[421] = $z.y;\n.O[422] = $z.z;\n.O[423] = $RightElbow.x;\n.O[424] = $RightElbow.y;\n.O[425] = $RightElbow.z;\n\nif (.I[235] == 0){\n    $z = $RightHand_Z * -1;\n    $x = unit(cross($low,$z));\n}else{\n    $x = $RightHand_Z;\n    $z = unit(cross($x,$low));\n}\n$y = cross($z,$x);\nvector $Right_hand_z = $z;\n.O[426] = $x.x;\n.O[427] = $x.y;\n.O[428] = $x.z;\n.O[429] = $y.x;\n.O[430] = $y.y;\n.O[431] = $y.z;\n.O[432] = $z.x;\n.O[433] = $z.y;\n.O[434] = $z.z;\n.O[435] = $RightHand.x;\n"
		+ ".O[436] = $RightHand.y;\n.O[437] = $RightHand.z;\n\n//match orientation from the hand\n\n\n//fingers\nvector $average = ($LeftThumb2+$LeftThumb)/2;\n$x = unit(cross($LeftThumb2-$LeftThumb, $average-$LeftThumb1));\nvector $y0 = unit($LeftThumb1-$LeftThumb) * 1;\n$z = cross($x, $y0);\n.O[438] = $x.x;\n.O[439] = $x.y;\n.O[440] = $x.z;\n.O[441] = $y0.x;\n.O[442] = $y0.y;\n.O[443] = $y0.z;\n.O[444] = $z.x;\n.O[445] = $z.y;\n.O[446] = $z.z;\n.O[447] = $LeftThumb.x;\n.O[448] = $LeftThumb.y;\n.O[449] = $LeftThumb.z;\nvector $y1 = unit($LeftThumb2-$LeftThumb1) * 1;\n$z = cross($x, $y1);\n.O[450] = $x.x;\n.O[451] = $x.y;\n.O[452] = $x.z;\n.O[453] = $y1.x;\n.O[454] = $y1.y;\n.O[455] = $y1.z;\n.O[456] = $z.x;\n.O[457] = $z.y;\n.O[458] = $z.z;\n.O[459] = $LeftThumb1.x;\n.O[460] = $LeftThumb1.y;\n.O[461] = $LeftThumb1.z;\n$y = rot($y1, $x, angle($y0,$y1));\n$z = cross($x, $y);\n.O[450] = $x.x;\n.O[451] = $x.y;\n.O[452] = $x.z;\n.O[453] = $y.x;\n.O[454] = $y.y;\n.O[455] = $y.z;\n.O[456] = $z.x;\n.O[457] = $z.y;\n.O[458] = $z.z;\n.O[459] = $LeftThumb2.x;\n.O[460] = $LeftThumb2.y;\n"
		+ ".O[461] = $LeftThumb2.z;\n$average = ($LeftIndexFinger2+$LeftIndexFinger)/2;\n$x = unit(cross($LeftIndexFinger2-$LeftIndexFinger, $average-$LeftIndexFinger1));\n$y0 = unit($LeftIndexFinger1-$LeftIndexFinger) * 1;\n$z = cross($x, $y0);\n.O[462] = $x.x;\n.O[463] = $x.y;\n.O[464] = $x.z;\n.O[465] = $y0.x;\n.O[466] = $y0.y;\n.O[467] = $y0.z;\n.O[468] = $z.x;\n.O[469] = $z.y;\n.O[470] = $z.z;\n.O[471] = $LeftIndexFinger.x;\n.O[472] = $LeftIndexFinger.y;\n.O[473] = $LeftIndexFinger.z;\n$y1 = unit($LeftIndexFinger2-$LeftIndexFinger1) * 1;\n$z = cross($x, $y1);\n.O[474] = $x.x;\n.O[475] = $x.y;\n.O[476] = $x.z;\n.O[477] = $y1.x;\n.O[478] = $y1.y;\n.O[479] = $y1.z;\n.O[480] = $z.x;\n.O[481] = $z.y;\n.O[482] = $z.z;\n.O[483] = $LeftIndexFinger1.x;\n.O[484] = $LeftIndexFinger1.y;\n.O[485] = $LeftIndexFinger1.z;\n$y = rot($y1, $x, angle($y0,$y1));\n$z = cross($x, $y);\n.O[474] = $x.x;\n.O[475] = $x.y;\n.O[476] = $x.z;\n.O[477] = $y.x;\n.O[478] = $y.y;\n.O[479] = $y.z;\n.O[480] = $z.x;\n.O[481] = $z.y;\n.O[482] = $z.z;\n.O[483] = $LeftIndexFinger2.x;\n.O[484] = $LeftIndexFinger2.y;\n"
		+ ".O[485] = $LeftIndexFinger2.z;\n$average = ($LeftMiddleFinger2+$LeftMiddleFinger)/2;\n$x = unit(cross($LeftMiddleFinger2-$LeftMiddleFinger, $average-$LeftMiddleFinger1));\n$y0 = unit($LeftMiddleFinger1-$LeftMiddleFinger) * 1;\n$z = cross($x, $y0);\n.O[486] = $x.x;\n.O[487] = $x.y;\n.O[488] = $x.z;\n.O[489] = $y0.x;\n.O[490] = $y0.y;\n.O[491] = $y0.z;\n.O[492] = $z.x;\n.O[493] = $z.y;\n.O[494] = $z.z;\n.O[495] = $LeftMiddleFinger.x;\n.O[496] = $LeftMiddleFinger.y;\n.O[497] = $LeftMiddleFinger.z;\n$y1 = unit($LeftMiddleFinger2-$LeftMiddleFinger1) * 1;\n$z = cross($x, $y1);\n.O[498] = $x.x;\n.O[499] = $x.y;\n.O[500] = $x.z;\n.O[501] = $y1.x;\n.O[502] = $y1.y;\n.O[503] = $y1.z;\n.O[504] = $z.x;\n.O[505] = $z.y;\n.O[506] = $z.z;\n.O[507] = $LeftMiddleFinger1.x;\n.O[508] = $LeftMiddleFinger1.y;\n.O[509] = $LeftMiddleFinger1.z;\n$y = rot($y1, $x, angle($y0,$y1));\n$z = cross($x, $y);\n.O[498] = $x.x;\n.O[499] = $x.y;\n.O[500] = $x.z;\n.O[501] = $y.x;\n.O[502] = $y.y;\n.O[503] = $y.z;\n.O[504] = $z.x;\n.O[505] = $z.y;\n.O[506] = $z.z;\n.O[507] = $LeftMiddleFinger2.x;\n"
		+ ".O[508] = $LeftMiddleFinger2.y;\n.O[509] = $LeftMiddleFinger2.z;\n$average = ($LeftRingFinger2+$LeftRingFinger)/2;\n$x = unit(cross($LeftRingFinger2-$LeftRingFinger, $average-$LeftRingFinger1));\n$y0 = unit($LeftRingFinger1-$LeftRingFinger) * 1;\n$z = cross($x, $y0);\n.O[510] = $x.x;\n.O[511] = $x.y;\n.O[512] = $x.z;\n.O[513] = $y0.x;\n.O[514] = $y0.y;\n.O[515] = $y0.z;\n.O[516] = $z.x;\n.O[517] = $z.y;\n.O[518] = $z.z;\n.O[519] = $LeftRingFinger.x;\n.O[520] = $LeftRingFinger.y;\n.O[521] = $LeftRingFinger.z;\n$y1 = unit($LeftRingFinger2-$LeftRingFinger1) * 1;\n$z = cross($x, $y1);\n.O[522] = $x.x;\n.O[523] = $x.y;\n.O[524] = $x.z;\n.O[525] = $y1.x;\n.O[526] = $y1.y;\n.O[527] = $y1.z;\n.O[528] = $z.x;\n.O[529] = $z.y;\n.O[530] = $z.z;\n.O[531] = $LeftRingFinger1.x;\n.O[532] = $LeftRingFinger1.y;\n.O[533] = $LeftRingFinger1.z;\n$y = rot($y1, $x, angle($y0,$y1));\n$z = cross($x, $y);\n.O[522] = $x.x;\n.O[523] = $x.y;\n.O[524] = $x.z;\n.O[525] = $y.x;\n.O[526] = $y.y;\n.O[527] = $y.z;\n.O[528] = $z.x;\n.O[529] = $z.y;\n.O[530] = $z.z;\n.O[531] = $LeftRingFinger2.x;\n"
		+ ".O[532] = $LeftRingFinger2.y;\n.O[533] = $LeftRingFinger2.z;\n$average = ($LeftPinkyFinger2+$LeftPinkyFinger)/2;\n$x = unit(cross($LeftPinkyFinger2-$LeftPinkyFinger, $average-$LeftPinkyFinger1));\n$y0 = unit($LeftPinkyFinger1-$LeftPinkyFinger) * 1;\n$z = cross($x, $y0);\n.O[534] = $x.x;\n.O[535] = $x.y;\n.O[536] = $x.z;\n.O[537] = $y0.x;\n.O[538] = $y0.y;\n.O[539] = $y0.z;\n.O[540] = $z.x;\n.O[541] = $z.y;\n.O[542] = $z.z;\n.O[543] = $LeftPinkyFinger.x;\n.O[544] = $LeftPinkyFinger.y;\n.O[545] = $LeftPinkyFinger.z;\n$y1 = unit($LeftPinkyFinger2-$LeftPinkyFinger1) * 1;\n$z = cross($x, $y1);\n.O[546] = $x.x;\n.O[547] = $x.y;\n.O[548] = $x.z;\n.O[549] = $y1.x;\n.O[550] = $y1.y;\n.O[551] = $y1.z;\n.O[552] = $z.x;\n.O[553] = $z.y;\n.O[554] = $z.z;\n.O[555] = $LeftPinkyFinger1.x;\n.O[556] = $LeftPinkyFinger1.y;\n.O[557] = $LeftPinkyFinger1.z;\n$y = rot($y1, $x, angle($y0,$y1));\n$z = cross($x, $y);\n.O[546] = $x.x;\n.O[547] = $x.y;\n.O[548] = $x.z;\n.O[549] = $y.x;\n.O[550] = $y.y;\n.O[551] = $y.z;\n.O[552] = $z.x;\n.O[553] = $z.y;\n.O[554] = $z.z;\n.O[555] = $LeftPinkyFinger2.x;\n"
		+ ".O[556] = $LeftPinkyFinger2.y;\n.O[557] = $LeftPinkyFinger2.z;\n$average = ($RightThumb2+$RightThumb)/2;\n$x = unit(cross($RightThumb2-$RightThumb, $average-$RightThumb1));\n$y0 = unit($RightThumb1-$RightThumb) * -1;\n$z = cross($x, $y0);\n.O[558] = $x.x;\n.O[559] = $x.y;\n.O[560] = $x.z;\n.O[561] = $y0.x;\n.O[562] = $y0.y;\n.O[563] = $y0.z;\n.O[564] = $z.x;\n.O[565] = $z.y;\n.O[566] = $z.z;\n.O[567] = $RightThumb.x;\n.O[568] = $RightThumb.y;\n.O[569] = $RightThumb.z;\n$y1 = unit($RightThumb2-$RightThumb1) * -1;\n$z = cross($x, $y1);\n.O[570] = $x.x;\n.O[571] = $x.y;\n.O[572] = $x.z;\n.O[573] = $y1.x;\n.O[574] = $y1.y;\n.O[575] = $y1.z;\n.O[576] = $z.x;\n.O[577] = $z.y;\n.O[578] = $z.z;\n.O[579] = $RightThumb1.x;\n.O[580] = $RightThumb1.y;\n.O[581] = $RightThumb1.z;\n$y = rot($y1, $x, angle($y0,$y1));\n$z = cross($x, $y);\n.O[570] = $x.x;\n.O[571] = $x.y;\n.O[572] = $x.z;\n.O[573] = $y.x;\n.O[574] = $y.y;\n.O[575] = $y.z;\n.O[576] = $z.x;\n.O[577] = $z.y;\n.O[578] = $z.z;\n.O[579] = $RightThumb2.x;\n.O[580] = $RightThumb2.y;\n.O[581] = $RightThumb2.z;\n$average = ($RightIndexFinger2+$RightIndexFinger)/2;\n"
		+ "$x = unit(cross($RightIndexFinger2-$RightIndexFinger, $average-$RightIndexFinger1));\n$y0 = unit($RightIndexFinger1-$RightIndexFinger) * -1;\n$z = cross($x, $y0);\n.O[582] = $x.x;\n.O[583] = $x.y;\n.O[584] = $x.z;\n.O[585] = $y0.x;\n.O[586] = $y0.y;\n.O[587] = $y0.z;\n.O[588] = $z.x;\n.O[589] = $z.y;\n.O[590] = $z.z;\n.O[591] = $RightIndexFinger.x;\n.O[592] = $RightIndexFinger.y;\n.O[593] = $RightIndexFinger.z;\n$y1 = unit($RightIndexFinger2-$RightIndexFinger1) * -1;\n$z = cross($x, $y1);\n.O[594] = $x.x;\n.O[595] = $x.y;\n.O[596] = $x.z;\n.O[597] = $y1.x;\n.O[598] = $y1.y;\n.O[599] = $y1.z;\n.O[600] = $z.x;\n.O[601] = $z.y;\n.O[602] = $z.z;\n.O[603] = $RightIndexFinger1.x;\n.O[604] = $RightIndexFinger1.y;\n.O[605] = $RightIndexFinger1.z;\n$y = rot($y1, $x, angle($y0,$y1));\n$z = cross($x, $y);\n.O[594] = $x.x;\n.O[595] = $x.y;\n.O[596] = $x.z;\n.O[597] = $y.x;\n.O[598] = $y.y;\n.O[599] = $y.z;\n.O[600] = $z.x;\n.O[601] = $z.y;\n.O[602] = $z.z;\n.O[603] = $RightIndexFinger2.x;\n.O[604] = $RightIndexFinger2.y;\n.O[605] = $RightIndexFinger2.z;\n$average = ($RightMiddleFinger2+$RightMiddleFinger)/2;\n"
		+ "$x = unit(cross($RightMiddleFinger2-$RightMiddleFinger, $average-$RightMiddleFinger1));\n$y0 = unit($RightMiddleFinger1-$RightMiddleFinger) * -1;\n$z = cross($x, $y0);\n.O[606] = $x.x;\n.O[607] = $x.y;\n.O[608] = $x.z;\n.O[609] = $y0.x;\n.O[610] = $y0.y;\n.O[611] = $y0.z;\n.O[612] = $z.x;\n.O[613] = $z.y;\n.O[614] = $z.z;\n.O[615] = $RightMiddleFinger.x;\n.O[616] = $RightMiddleFinger.y;\n.O[617] = $RightMiddleFinger.z;\n$y1 = unit($RightMiddleFinger2-$RightMiddleFinger1) * -1;\n$z = cross($x, $y1);\n.O[618] = $x.x;\n.O[619] = $x.y;\n.O[620] = $x.z;\n.O[621] = $y1.x;\n.O[622] = $y1.y;\n.O[623] = $y1.z;\n.O[624] = $z.x;\n.O[625] = $z.y;\n.O[626] = $z.z;\n.O[627] = $RightMiddleFinger1.x;\n.O[628] = $RightMiddleFinger1.y;\n.O[629] = $RightMiddleFinger1.z;\n$y = rot($y1, $x, angle($y0,$y1));\n$z = cross($x, $y);\n.O[618] = $x.x;\n.O[619] = $x.y;\n.O[620] = $x.z;\n.O[621] = $y.x;\n.O[622] = $y.y;\n.O[623] = $y.z;\n.O[624] = $z.x;\n.O[625] = $z.y;\n.O[626] = $z.z;\n.O[627] = $RightMiddleFinger2.x;\n.O[628] = $RightMiddleFinger2.y;\n.O[629] = $RightMiddleFinger2.z;\n"
		+ "$average = ($RightRingFinger2+$RightRingFinger)/2;\n$x = unit(cross($RightRingFinger2-$RightRingFinger, $average-$RightRingFinger1));\n$y0 = unit($RightRingFinger1-$RightRingFinger) * -1;\n$z = cross($x, $y0);\n.O[630] = $x.x;\n.O[631] = $x.y;\n.O[632] = $x.z;\n.O[633] = $y0.x;\n.O[634] = $y0.y;\n.O[635] = $y0.z;\n.O[636] = $z.x;\n.O[637] = $z.y;\n.O[638] = $z.z;\n.O[639] = $RightRingFinger.x;\n.O[640] = $RightRingFinger.y;\n.O[641] = $RightRingFinger.z;\n$y1 = unit($RightRingFinger2-$RightRingFinger1) * -1;\n$z = cross($x, $y1);\n.O[642] = $x.x;\n.O[643] = $x.y;\n.O[644] = $x.z;\n.O[645] = $y1.x;\n.O[646] = $y1.y;\n.O[647] = $y1.z;\n.O[648] = $z.x;\n.O[649] = $z.y;\n.O[650] = $z.z;\n.O[651] = $RightRingFinger1.x;\n.O[652] = $RightRingFinger1.y;\n.O[653] = $RightRingFinger1.z;\n$y = rot($y1, $x, angle($y0,$y1));\n$z = cross($x, $y);\n.O[642] = $x.x;\n.O[643] = $x.y;\n.O[644] = $x.z;\n.O[645] = $y.x;\n.O[646] = $y.y;\n.O[647] = $y.z;\n.O[648] = $z.x;\n.O[649] = $z.y;\n.O[650] = $z.z;\n.O[651] = $RightRingFinger2.x;\n.O[652] = $RightRingFinger2.y;\n.O[653] = $RightRingFinger2.z;\n"
		+ "$average = ($RightPinkyFinger2+$RightPinkyFinger)/2;\n$x = unit(cross($RightPinkyFinger2-$RightPinkyFinger, $average-$RightPinkyFinger1));\n$y0 = unit($RightPinkyFinger1-$RightPinkyFinger) * -1;\n$z = cross($x, $y0);\n.O[654] = $x.x;\n.O[655] = $x.y;\n.O[656] = $x.z;\n.O[657] = $y0.x;\n.O[658] = $y0.y;\n.O[659] = $y0.z;\n.O[660] = $z.x;\n.O[661] = $z.y;\n.O[662] = $z.z;\n.O[663] = $RightPinkyFinger.x;\n.O[664] = $RightPinkyFinger.y;\n.O[665] = $RightPinkyFinger.z;\n$y1 = unit($RightPinkyFinger2-$RightPinkyFinger1) * -1;\n$z = cross($x, $y1);\n.O[666] = $x.x;\n.O[667] = $x.y;\n.O[668] = $x.z;\n.O[669] = $y1.x;\n.O[670] = $y1.y;\n.O[671] = $y1.z;\n.O[672] = $z.x;\n.O[673] = $z.y;\n.O[674] = $z.z;\n.O[675] = $RightPinkyFinger1.x;\n.O[676] = $RightPinkyFinger1.y;\n.O[677] = $RightPinkyFinger1.z;\n$y = rot($y1, $x, angle($y0,$y1));\n$z = cross($x, $y);\n.O[666] = $x.x;\n.O[667] = $x.y;\n.O[668] = $x.z;\n.O[669] = $y.x;\n.O[670] = $y.y;\n.O[671] = $y.z;\n.O[672] = $z.x;\n.O[673] = $z.y;\n.O[674] = $z.z;\n.O[675] = $RightPinkyFinger2.x;\n.O[676] = $RightPinkyFinger2.y;\n"
		+ ".O[677] = $RightPinkyFinger2.z;");
createNode pointMatrixMult -n "RightBigToe";
	rename -uid "9ADB4BBA-4BD5-615B-AC85-C9BDD94C57A3";
createNode fourByFourMatrix -n "Lf_finger_ring_2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Lf_arm_fk3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "RightRingFinger1";
	rename -uid "60176099-4F3C-7EED-8D26-489ACF719EA9";
createNode pointMatrixMult -n "RightRingFinger2";
	rename -uid "0A346D8D-4F4D-4A39-72C4-2D964DC9E7F2";
createNode fourByFourMatrix -n "Lf_finger_thumb_1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Rt_arm_ik_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "RingFinger_point";
	rename -uid "28BAE91E-4382-E569-F33F-B3B3E370E9AE";
createNode pointMatrixMult -n "LeftRingFinger_Z";
	rename -uid "760A14E4-422A-72DF-AA22-52B76F09419D";
createNode fourByFourMatrix -n "Lf_leg_fk1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "spine_chest_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "pointMatrixMult1";
	rename -uid "A7BD85A5-43AA-F6FC-56CA-D79E4F6E9591";
createNode file -n "file3";
	rename -uid "F8EB86FA-4BAE-EAA5-05DA-7D9F41D6FB5E";
	setAttr ".ail" yes;
	setAttr ".ftn" -type "string" "C:/Users/morga/Downloads/Cartwheel-Happy_barefoot_dancing.fbm/tex_g_NRM.png";
	setAttr ".cs" -type "string" "sRGB";
createNode fourByFourMatrix -n "Lf_arm_fk1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftThumb_Z";
	rename -uid "E8F56F1E-4B37-33F0-4D2A-AF86464501C1";
createNode pointMatrixMult -n "LeftRingFinger2";
	rename -uid "5311AAAB-49A8-4D45-C22E-9C9468BBB897";
createNode fourByFourMatrix -n "Lf_leg_ik_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode aiAOVDriver -s -n "defaultArnoldDriver";
	rename -uid "CF211592-45DC-8204-F449-18B3CE04AB5A";
	setAttr ".ai_translator" -type "string" "exr";
createNode pointMatrixMult -n "RightPinkyFinger2";
	rename -uid "EE59D4A9-45EF-CE62-E290-83B13B3165FA";
createNode fourByFourMatrix -n "Rt_arm_fk2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "RightRingFinger_Z";
	rename -uid "A8824E25-4DCE-D7FC-3778-BC8A5DAC98F9";
createNode pointMatrixMult -n "RightCollar_Z";
	rename -uid "8501AEEF-4164-4370-0B5E-1ABFD0644B74";
createNode fourByFourMatrix -n "Lf_finger_ring_1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftPinkyFinger2";
	rename -uid "47D118BC-43FF-D9CE-6E64-738609CBC3CC";
createNode fourByFourMatrix -n "Lf_finger_thumb_2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Rt_finger_mid_3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Lf_finger_index_3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
	setAttr ".i00" 0.0011446829837590891;
	setAttr ".i01" -2.0978287065172959e-06;
	setAttr ".i02" -0.99999934484801833;
	setAttr ".i10" 0.99999934484073638;
	setAttr ".i11" -4.3524410960090667e-06;
	setAttr ".i12" 0.0011446829928814354;
	setAttr ".i20" -4.3548395933409868e-06;
	setAttr ".i21" -0.99999999998832767;
	setAttr ".i22" 2.0928451668449703e-06;
	setAttr ".i30" 77.154255487414616;
	setAttr ".i31" 127.01276168478817;
	setAttr ".i32" -1.6094018507676959;
createNode fourByFourMatrix -n "Lf_arm_fk2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftRingFinger";
	rename -uid "EA4E5D24-41A2-5732-872F-6ABE2FDD6D71";
createNode pointMatrixMult -n "LeftThumb2";
	rename -uid "BE0E90EC-4AF1-54DA-DE5E-FD807F59F5F9";
createNode fourByFourMatrix -n "Rt_leg_fk2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Lf_finger_index_1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode shadingEngine -n "pCube1_geo_dup_geoSG";
	rename -uid "F2507707-44D2-04CC-28F3-959B9A27C876";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode fourByFourMatrix -n "Lf_leg_pv_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "RightToe_Y";
	rename -uid "9A418361-460A-F798-E682-2FB60E2FEF3B";
createNode pointMatrixMult -n "LeftIndexFinger_Z";
	rename -uid "4628BB0C-45CA-1459-C926-0C810A29E8F8";
createNode pointMatrixMult -n "LeftCollar_Z";
	rename -uid "C19464D4-46E4-64CE-797D-B18FFE6F001D";
createNode pointMatrixMult -n "RightThumb2";
	rename -uid "5B482914-49DE-8580-258B-1982117D29AE";
createNode fourByFourMatrix -n "Rt_leg_ik_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftIndexFinger1";
	rename -uid "F5B35DE3-4576-9869-BEB3-BE94050C7C47";
createNode fourByFourMatrix -n "Lf_finger_pinky_3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "RightRingFinger";
	rename -uid "B7EDB99C-453A-B8DD-BAB9-B4874BDD210A";
createNode fourByFourMatrix -n "Lf_finger_mid_2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "RightPinkyFinger_Z";
	rename -uid "04A2D1A4-4C93-19D7-5098-AE8BB2437A7D";
createNode fourByFourMatrix -n "Rt_leg_fk1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Rt_finger_index_1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Lf_finger_mid_3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftToe_Y";
	rename -uid "DF1BDBBF-431C-B69C-6360-F7909443C456";
createNode pointMatrixMult -n "LeftPinkyFinger";
	rename -uid "BF16EF2C-4BBB-8D53-7241-DEB7DAB98B56";
createNode aiAOVFilter -s -n "defaultArnoldFilter";
	rename -uid "94FF0259-413F-24B7-ED91-5CBFA527625A";
	setAttr ".ai_translator" -type "string" "gaussian";
createNode pointMatrixMult -n "RightIndexFinger1";
	rename -uid "EFC3B5E8-4535-3775-78E6-EEB10D8EB1FC";
createNode pointMatrixMult -n "RightThumb";
	rename -uid "9B8C016A-462E-8146-DC18-70BD4273CB5B";
createNode pointMatrixMult -n "RightMiddleFinger_Z";
	rename -uid "680A5BED-447C-ADBE-80AE-A59ED1C705F4";
createNode pointMatrixMult -n "RightMiddleFinger2";
	rename -uid "DEB39AFA-496C-A89F-C76A-088EA058BF3D";
createNode fourByFourMatrix -n "Rt_finger_thumb_3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Rt_arm_fk1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftMiddleFinger1";
	rename -uid "4D20BE4C-4BDB-4038-8597-7898404325C3";
createNode fourByFourMatrix -n "Rt_finger_ring_1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Lf_finger_pinky_2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftThumb1";
	rename -uid "5F4CC0D4-4CC5-64A1-BB81-1A9B891B7F0B";
createNode pointMatrixMult -n "RightPinkyToe";
	rename -uid "67506131-4DB4-A893-D60B-3383A830BF6C";
createNode fourByFourMatrix -n "Lf_arm_clav_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftIndexFinger";
	rename -uid "0EA0CCA5-4146-E3FE-1D92-C48561455044";
createNode fourByFourMatrix -n "Lf_finger_pinky_1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftMiddleToe";
	rename -uid "C7CF39AE-4650-21F9-0676-D78876286027";
createNode pointMatrixMult -n "RightThumb_Z";
	rename -uid "BF262D2D-42CD-5DF3-FBC7-AA80247AF400";
createNode fourByFourMatrix -n "Rt_leg_pv_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Rt_arm_clav_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode aiAOVDriver -s -n "defaultArnoldDisplayDriver";
	rename -uid "B38B979B-471E-B5E5-657A-CFB57CF50497";
	setAttr ".output_mode" 0;
	setAttr ".ai_translator" -type "string" "maya";
createNode pointMatrixMult -n "LeftThumb";
	rename -uid "2BD3CB5C-4D81-CA2A-C0F3-06B6EA2F2C7A";
createNode pointMatrixMult -n "LeftIndexToe";
	rename -uid "BAADE725-4DE6-9E70-DC4F-04BB81A02BD0";
createNode fourByFourMatrix -n "Rt_leg_fk3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "head_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Rt_finger_index_3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Lf_arm_ik_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Rt_arm_pv_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftMiddleFinger";
	rename -uid "F863D266-4189-F63D-3F79-0582FF6E1479";
createNode fourByFourMatrix -n "Lf_leg_fk3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftPinkyFinger1";
	rename -uid "CBF15EB9-4663-9CE4-3C57-CCAD39CC07C1";
createNode pointMatrixMult -n "RightIndexFinger";
	rename -uid "33F138AF-4EAE-B8BD-354F-5EACAEA7150B";
createNode pointMatrixMult -n "RightMiddleFinger";
	rename -uid "2C0EC03E-4573-D679-F379-56A642BFE613";
createNode pointMatrixMult -n "RightIndexFinger_Z";
	rename -uid "586C5308-492C-636A-F1AD-A3BFB7B641F3";
createNode fourByFourMatrix -n "Rt_arm_fk3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftToe_X";
	rename -uid "7C626D6E-4BE9-E06E-2F6F-80BEB2E2EAA6";
createNode pointMatrixMult -n "RightPinkyFinger";
	rename -uid "8765BEC3-4F1C-AD98-283C-97BB8FD036C3";
createNode fourByFourMatrix -n "Rt_finger_ring_2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "RightIndexFinger2";
	rename -uid "5A7A9587-40BC-F7F8-233E-17ABB16A7D4A";
createNode fourByFourMatrix -n "Lf_finger_thumb_3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Rt_finger_pinky_3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "RightThumb1";
	rename -uid "6F93547B-4489-847C-171E-B0B84E56206F";
createNode fourByFourMatrix -n "Rt_finger_pinky_2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftRingToe";
	rename -uid "3FEFB2D5-4D1D-2326-4160-8BB49873953C";
createNode fourByFourMatrix -n "Lf_finger_ring_3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "hips_opm";
	rename -uid "6617305E-47AA-6953-E161-2699A87EB727";
	setAttr ".i00" 0.73731797511440045;
	setAttr ".i01" 0.014495946072134818;
	setAttr ".i02" 0.67539031020638285;
	setAttr ".i10" 0.068026509618886413;
	setAttr ".i11" 0.99309469904805658;
	setAttr ".i12" -0.095578829830258255;
	setAttr ".i20" -0.67211204241723854;
	setAttr ".i21" 0.11641643470800705;
	setAttr ".i22" 0.73124046398404707;
	setAttr ".i30" 3.3088721235242211;
	setAttr ".i31" 71.157347535509757;
	setAttr ".i32" -10.418728488139005;
createNode fourByFourMatrix -n "Lf_leg_fk2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "RightMiddleFinger1";
	rename -uid "34200729-48B0-3ED0-861D-909F6575F006";
createNode pointMatrixMult -n "RightMiddleToe";
	rename -uid "08294BA5-448E-A544-6739-10BC88DCDB9D";
createNode lambert -n "wood";
	rename -uid "D0E77788-498B-2229-51A8-9D9FA2F9D014";
createNode pointMatrixMult -n "LeftIndexFinger2";
	rename -uid "AD87EFE9-421C-70CD-F59C-1089477B7786";
createNode fourByFourMatrix -n "Rt_finger_ring_3_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode file -n "file2";
	rename -uid "F915B852-4F63-6281-FA6A-7F85B0BF648F";
	setAttr ".ftn" -type "string" "C:/Users/morga/Downloads/Cartwheel-Happy_barefoot_dancing.fbm/tex_g_COLOR.png";
	setAttr ".cs" -type "string" "sRGB";
createNode aiOptions -s -n "defaultArnoldRenderOptions";
	rename -uid "5830BA62-48F7-3813-1470-988D98F40930";
	setAttr ".version" -type "string" "3.2.2";
createNode fourByFourMatrix -n "Lf_finger_index_2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftPinkyToe";
	rename -uid "8A8E40FC-4EF1-14C6-0762-B698395917F5";
createNode fourByFourMatrix -n "Rt_finger_index_2_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftRingFinger1";
	rename -uid "21BDFE82-4DF8-C524-D42D-569C51221DE8";
createNode pointMatrixMult -n "LeftPinkyFinger_Z";
	rename -uid "E831F4EA-47C6-E7B0-EDC2-56AFF3BB0502";
createNode pointMatrixMult -n "RightRingToe";
	rename -uid "A9CF2F76-4006-01ED-3B45-018AF109DBD6";
createNode fourByFourMatrix -n "Lf_finger_mid_1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftMiddleFinger_Z";
	rename -uid "335657F9-44D4-157E-2DC0-E8B0F6451394";
createNode fourByFourMatrix -n "root_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode fourByFourMatrix -n "Lf_arm_pv_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "LeftBigToe";
	rename -uid "19A7262D-4666-25CD-F020-7785B2D0A614";
createNode bump2d -n "bump2d1";
	rename -uid "CE7700DB-4B6D-5997-416B-5E8908E05C94";
	setAttr ".bd" 0.34999999403953552;
	setAttr ".bi" 1;
	setAttr ".vc1" -type "float3" 0 9.9999997e-06 0 ;
	setAttr ".vc2" -type "float3" 9.9999997e-06 9.9999997e-06 0 ;
createNode place2dTexture -n "place2dTexture1";
	rename -uid "BCD520EF-4CEC-2387-9736-EB93D73743B1";
createNode materialInfo -n "materialInfo1";
	rename -uid "6DA10AFA-4BD4-2078-BB44-64BE063C42B5";
createNode fourByFourMatrix -n "Rt_finger_thumb_1_opm";
	rename -uid "9A735825-40BD-E23C-53AC-C685A76F7B75";
createNode pointMatrixMult -n "RightToe_X";
	rename -uid "A0FBE895-4E58-0011-2C86-E880C998809E";
createNode pointMatrixMult -n "LeftMiddleFinger2";
	rename -uid "E2162977-4B43-B30D-048B-F3963F317A38";
createNode pointMatrixMult -n "RightIndexToe";
	rename -uid "62F59BDE-437A-4720-4491-C3B87745E258";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "010FB738-48D3-A1D3-064A-F39FAE445453";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 7;
	setAttr -av -k on ".unw" 7;
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".fzn";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".rm";
	setAttr -av -k on ".lm";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -av -k on ".hom";
	setAttr -av -k on ".hodm";
	setAttr -av -k on ".xry";
	setAttr -av -k on ".jxr";
	setAttr -av -k on ".sslt";
	setAttr -av -k on ".cbr";
	setAttr -av -k on ".bbr";
	setAttr -av -k on ".mhl";
	setAttr -k on ".cons";
	setAttr -k on ".vac";
	setAttr -av -k on ".hwi";
	setAttr -k on ".csvd";
	setAttr -av -k on ".ta";
	setAttr -av -k on ".tq";
	setAttr -k on ".ts";
	setAttr -av -k on ".etmr";
	setAttr -k on ".tmrm";
	setAttr -av -k on ".tmr";
	setAttr -av -k on ".aoon";
	setAttr -av -k on ".aoam";
	setAttr -av -k on ".aora";
	setAttr -av -k on ".aofr";
	setAttr -av -k on ".aosm";
	setAttr -av -k on ".hff";
	setAttr -av -k on ".hfd";
	setAttr -av -k on ".hfs";
	setAttr -av -k on ".hfe";
	setAttr -av ".hfc";
	setAttr -av -k on ".hfcr";
	setAttr -av -k on ".hfcg";
	setAttr -av -k on ".hfcb";
	setAttr -av -k on ".hfa";
	setAttr -av -k on ".mbe";
	setAttr -av -k on ".mbt";
	setAttr -av -k on ".mbsof";
	setAttr -k on ".mbsc";
	setAttr -k on ".mbc";
	setAttr -k on ".mbfa";
	setAttr -k on ".mbftb";
	setAttr -k on ".mbftg";
	setAttr -k on ".mbftr";
	setAttr -av -k on ".mbfta";
	setAttr -k on ".mbfe";
	setAttr -k on ".mbme";
	setAttr -av -k on ".mbcsx";
	setAttr -av -k on ".mbcsy";
	setAttr -av -k on ".mbasx";
	setAttr -av -k on ".mbasy";
	setAttr -av -k on ".blen";
	setAttr -av -k on ".blth";
	setAttr -av -k on ".blfr";
	setAttr -av -k on ".blfa";
	setAttr -av -k on ".blat";
	setAttr -av -k on ".msaa";
	setAttr -av -k on ".aasc";
	setAttr -av -k on ".aasq";
	setAttr -k on ".laa";
	setAttr -k on ".gamm";
	setAttr -k on ".gmmv";
	setAttr -k on ".fprt" yes;
	setAttr -k on ".rtfm";
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 3 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 6 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 59 ".u";
select -ne :defaultRenderingList1;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultTextureList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".tx";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -k on ".mwc";
	setAttr -av -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -k on ".hio";
	setAttr -cb on ".ai_override";
	setAttr -k on ".ai_surface_shader";
	setAttr -cb on ".ai_surface_shaderr";
	setAttr -cb on ".ai_surface_shaderg";
	setAttr -cb on ".ai_surface_shaderb";
	setAttr -k on ".ai_volume_shader";
	setAttr -cb on ".ai_volume_shaderr";
	setAttr -cb on ".ai_volume_shaderg";
	setAttr -cb on ".ai_volume_shaderb";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -k on ".mwc";
	setAttr -av -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -k on ".hio";
	setAttr -cb on ".ai_override";
	setAttr -k on ".ai_surface_shader";
	setAttr -cb on ".ai_surface_shaderr";
	setAttr -cb on ".ai_surface_shaderg";
	setAttr -cb on ".ai_surface_shaderb";
	setAttr -k on ".ai_volume_shader";
	setAttr -cb on ".ai_volume_shaderr";
	setAttr -cb on ".ai_volume_shaderg";
	setAttr -cb on ".ai_volume_shaderb";
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".macc";
	setAttr -av -k on ".macd";
	setAttr -av -k on ".macq";
	setAttr -av -k on ".mcfr";
	setAttr -cb on ".ifg";
	setAttr -av -k on ".clip";
	setAttr -av -k on ".edm";
	setAttr -av -k on ".edl";
	setAttr -av -cb on ".ren";
	setAttr -av -k on ".esr";
	setAttr -av -k on ".ors";
	setAttr -cb on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -av -cb on ".imfkey";
	setAttr -av -k on ".gama";
	setAttr -av -k on ".exrc";
	setAttr -av -k on ".expt";
	setAttr -av -k on ".an";
	setAttr -cb on ".ar";
	setAttr -av -k on ".fs";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -av -cb on ".me";
	setAttr -cb on ".se";
	setAttr -av -k on ".be";
	setAttr -av -cb on ".ep";
	setAttr -av -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -cb on ".ofe";
	setAttr -cb on ".efe";
	setAttr -cb on ".oft";
	setAttr -cb on ".umfn";
	setAttr -cb on ".ufe";
	setAttr -av -cb on ".pff";
	setAttr -av -cb on ".peie";
	setAttr -av -cb on ".ifp";
	setAttr -k on ".rv";
	setAttr -av -k on ".comp";
	setAttr -av -k on ".cth";
	setAttr -av -k on ".soll";
	setAttr -av -cb on ".sosl";
	setAttr -av -k on ".rd";
	setAttr -av -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -av -k on ".shs";
	setAttr -av -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -av -k on ".mm";
	setAttr -av -k on ".npu";
	setAttr -av -k on ".itf";
	setAttr -av -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -av -k on ".uf";
	setAttr -av -k on ".oi";
	setAttr -av -k on ".rut";
	setAttr -av -k on ".mot";
	setAttr -av -k on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -av -k on ".mbso";
	setAttr -av -k on ".mbsc";
	setAttr -av -k on ".afp";
	setAttr -av -k on ".pfb";
	setAttr -av -k on ".pram";
	setAttr -av -k on ".poam";
	setAttr -av -k on ".prlm";
	setAttr -av -k on ".polm";
	setAttr -av -cb on ".prm";
	setAttr -av -cb on ".pom";
	setAttr -cb on ".pfrm";
	setAttr -cb on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -av -k on ".ubc";
	setAttr -av -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -av -k on ".udbx";
	setAttr -av -k on ".smc";
	setAttr -av -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -av -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -av -k on ".tlwd";
	setAttr -av -k on ".tlht";
	setAttr -av -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -av -k on ".ope";
	setAttr -av -k on ".oppf";
	setAttr -av -k on ".rcp";
	setAttr -av -k on ".icp";
	setAttr -av -k on ".ocp";
	setAttr -cb on ".hbl";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :defaultColorMgtGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -av -k off -cb on ".fbfm";
	setAttr -av -k off -cb on ".ehql";
	setAttr -av -k off -cb on ".eams";
	setAttr -av -k off -cb on ".eeaa";
	setAttr -av -k off -cb on ".engm";
	setAttr -av -k off -cb on ".mes";
	setAttr -av -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -av -k off -cb on ".mbs";
	setAttr -av -k off -cb on ".trm";
	setAttr -av -k off -cb on ".tshc";
	setAttr -av -k off -cb on ".enpt";
	setAttr -av -k off -cb on ".clmt";
	setAttr -av -k off -cb on ".tcov";
	setAttr -av -k off -cb on ".lith";
	setAttr -av -k off -cb on ".sobc";
	setAttr -av -k off -cb on ".cuth";
	setAttr -av -k off -cb on ".hgcd";
	setAttr -av -k off -cb on ".hgci";
	setAttr -av -k off -cb on ".mgcs";
	setAttr -av -k off -cb on ".twa";
	setAttr -av -k off -cb on ".twz";
	setAttr -av -cb on ".hwcc";
	setAttr -av -cb on ".hwdp";
	setAttr -av -cb on ".hwql";
	setAttr -av -k on ".hwfr";
	setAttr -av -k on ".soll";
	setAttr -av -k on ".sosl";
	setAttr -av -k on ".bswa";
	setAttr -av -k on ".shml";
	setAttr -av -k on ".hwel";
connectAttr "solver.out[150]" "retarget.left_prevX";
connectAttr "solver.out[151]" "retarget.left_prevY";
connectAttr "solver.out[152]" "retarget.left_prevZ";
connectAttr "solver.out[153]" "retarget.right_prevX";
connectAttr "solver.out[154]" "retarget.right_prevY";
connectAttr "solver.out[155]" "retarget.right_prevZ";
connectAttr "solver.out[210]" "LeftLegShape.cp[0].xv";
connectAttr "solver.out[211]" "LeftLegShape.cp[0].yv";
connectAttr "solver.out[212]" "LeftLegShape.cp[0].zv";
connectAttr "solver.out[213]" "LeftLegShape.cp[1].xv";
connectAttr "solver.out[214]" "LeftLegShape.cp[1].yv";
connectAttr "solver.out[215]" "LeftLegShape.cp[1].zv";
connectAttr "solver.out[216]" "LeftLegShape.cp[2].xv";
connectAttr "solver.out[217]" "LeftLegShape.cp[2].yv";
connectAttr "solver.out[218]" "LeftLegShape.cp[2].zv";
connectAttr "solver.out[219]" "RightLegShape.cp[0].xv";
connectAttr "solver.out[220]" "RightLegShape.cp[0].yv";
connectAttr "solver.out[221]" "RightLegShape.cp[0].zv";
connectAttr "solver.out[222]" "RightLegShape.cp[1].xv";
connectAttr "solver.out[223]" "RightLegShape.cp[1].yv";
connectAttr "solver.out[224]" "RightLegShape.cp[1].zv";
connectAttr "solver.out[225]" "RightLegShape.cp[2].xv";
connectAttr "solver.out[226]" "RightLegShape.cp[2].yv";
connectAttr "solver.out[227]" "RightLegShape.cp[2].zv";
connectAttr "solver.out[123]" "RightPinkyFingerShape.cp[0].xv";
connectAttr "solver.out[124]" "RightPinkyFingerShape.cp[0].yv";
connectAttr "solver.out[125]" "RightPinkyFingerShape.cp[0].zv";
connectAttr "solver.out[126]" "RightPinkyFingerShape.cp[1].xv";
connectAttr "solver.out[127]" "RightPinkyFingerShape.cp[1].yv";
connectAttr "solver.out[128]" "RightPinkyFingerShape.cp[1].zv";
connectAttr "solver.out[129]" "RightPinkyFingerShape.cp[2].xv";
connectAttr "solver.out[130]" "RightPinkyFingerShape.cp[2].yv";
connectAttr "solver.out[131]" "RightPinkyFingerShape.cp[2].zv";
connectAttr "solver.out[132]" "RightPinkyFingerShape.cp[3].xv";
connectAttr "solver.out[133]" "RightPinkyFingerShape.cp[3].yv";
connectAttr "solver.out[134]" "RightPinkyFingerShape.cp[3].zv";
connectAttr "solver.out[111]" "RightRingFingerShape.cp[0].xv";
connectAttr "solver.out[112]" "RightRingFingerShape.cp[0].yv";
connectAttr "solver.out[113]" "RightRingFingerShape.cp[0].zv";
connectAttr "solver.out[114]" "RightRingFingerShape.cp[1].xv";
connectAttr "solver.out[115]" "RightRingFingerShape.cp[1].yv";
connectAttr "solver.out[116]" "RightRingFingerShape.cp[1].zv";
connectAttr "solver.out[117]" "RightRingFingerShape.cp[2].xv";
connectAttr "solver.out[118]" "RightRingFingerShape.cp[2].yv";
connectAttr "solver.out[119]" "RightRingFingerShape.cp[2].zv";
connectAttr "solver.out[120]" "RightRingFingerShape.cp[3].xv";
connectAttr "solver.out[121]" "RightRingFingerShape.cp[3].yv";
connectAttr "solver.out[122]" "RightRingFingerShape.cp[3].zv";
connectAttr "solver.out[99]" "RightMiddleFingerShape.cp[0].xv";
connectAttr "solver.out[100]" "RightMiddleFingerShape.cp[0].yv";
connectAttr "solver.out[101]" "RightMiddleFingerShape.cp[0].zv";
connectAttr "solver.out[102]" "RightMiddleFingerShape.cp[1].xv";
connectAttr "solver.out[103]" "RightMiddleFingerShape.cp[1].yv";
connectAttr "solver.out[104]" "RightMiddleFingerShape.cp[1].zv";
connectAttr "solver.out[105]" "RightMiddleFingerShape.cp[2].xv";
connectAttr "solver.out[106]" "RightMiddleFingerShape.cp[2].yv";
connectAttr "solver.out[107]" "RightMiddleFingerShape.cp[2].zv";
connectAttr "solver.out[108]" "RightMiddleFingerShape.cp[3].xv";
connectAttr "solver.out[109]" "RightMiddleFingerShape.cp[3].yv";
connectAttr "solver.out[110]" "RightMiddleFingerShape.cp[3].zv";
connectAttr "solver.out[87]" "RightIndexFingerShape.cp[0].xv";
connectAttr "solver.out[88]" "RightIndexFingerShape.cp[0].yv";
connectAttr "solver.out[89]" "RightIndexFingerShape.cp[0].zv";
connectAttr "solver.out[90]" "RightIndexFingerShape.cp[1].xv";
connectAttr "solver.out[91]" "RightIndexFingerShape.cp[1].yv";
connectAttr "solver.out[92]" "RightIndexFingerShape.cp[1].zv";
connectAttr "solver.out[93]" "RightIndexFingerShape.cp[2].xv";
connectAttr "solver.out[94]" "RightIndexFingerShape.cp[2].yv";
connectAttr "solver.out[95]" "RightIndexFingerShape.cp[2].zv";
connectAttr "solver.out[96]" "RightIndexFingerShape.cp[3].xv";
connectAttr "solver.out[97]" "RightIndexFingerShape.cp[3].yv";
connectAttr "solver.out[98]" "RightIndexFingerShape.cp[3].zv";
connectAttr "solver.out[75]" "RightThumbShape.cp[0].xv";
connectAttr "solver.out[76]" "RightThumbShape.cp[0].yv";
connectAttr "solver.out[77]" "RightThumbShape.cp[0].zv";
connectAttr "solver.out[78]" "RightThumbShape.cp[1].xv";
connectAttr "solver.out[79]" "RightThumbShape.cp[1].yv";
connectAttr "solver.out[80]" "RightThumbShape.cp[1].zv";
connectAttr "solver.out[81]" "RightThumbShape.cp[2].xv";
connectAttr "solver.out[82]" "RightThumbShape.cp[2].yv";
connectAttr "solver.out[83]" "RightThumbShape.cp[2].zv";
connectAttr "solver.out[84]" "RightThumbShape.cp[3].xv";
connectAttr "solver.out[85]" "RightThumbShape.cp[3].yv";
connectAttr "solver.out[86]" "RightThumbShape.cp[3].zv";
connectAttr "solver.out[48]" "LeftPinkyFingerShape.cp[0].xv";
connectAttr "solver.out[49]" "LeftPinkyFingerShape.cp[0].yv";
connectAttr "solver.out[50]" "LeftPinkyFingerShape.cp[0].zv";
connectAttr "solver.out[51]" "LeftPinkyFingerShape.cp[1].xv";
connectAttr "solver.out[52]" "LeftPinkyFingerShape.cp[1].yv";
connectAttr "solver.out[53]" "LeftPinkyFingerShape.cp[1].zv";
connectAttr "solver.out[54]" "LeftPinkyFingerShape.cp[2].xv";
connectAttr "solver.out[55]" "LeftPinkyFingerShape.cp[2].yv";
connectAttr "solver.out[56]" "LeftPinkyFingerShape.cp[2].zv";
connectAttr "solver.out[57]" "LeftPinkyFingerShape.cp[3].xv";
connectAttr "solver.out[58]" "LeftPinkyFingerShape.cp[3].yv";
connectAttr "solver.out[59]" "LeftPinkyFingerShape.cp[3].zv";
connectAttr "solver.out[36]" "LeftRingFingerShape.cp[0].xv";
connectAttr "solver.out[37]" "LeftRingFingerShape.cp[0].yv";
connectAttr "solver.out[38]" "LeftRingFingerShape.cp[0].zv";
connectAttr "solver.out[39]" "LeftRingFingerShape.cp[1].xv";
connectAttr "solver.out[40]" "LeftRingFingerShape.cp[1].yv";
connectAttr "solver.out[41]" "LeftRingFingerShape.cp[1].zv";
connectAttr "solver.out[42]" "LeftRingFingerShape.cp[2].xv";
connectAttr "solver.out[43]" "LeftRingFingerShape.cp[2].yv";
connectAttr "solver.out[44]" "LeftRingFingerShape.cp[2].zv";
connectAttr "solver.out[45]" "LeftRingFingerShape.cp[3].xv";
connectAttr "solver.out[46]" "LeftRingFingerShape.cp[3].yv";
connectAttr "solver.out[47]" "LeftRingFingerShape.cp[3].zv";
connectAttr "solver.out[24]" "LeftMiddleFingerShape.cp[0].xv";
connectAttr "solver.out[25]" "LeftMiddleFingerShape.cp[0].yv";
connectAttr "solver.out[26]" "LeftMiddleFingerShape.cp[0].zv";
connectAttr "solver.out[27]" "LeftMiddleFingerShape.cp[1].xv";
connectAttr "solver.out[28]" "LeftMiddleFingerShape.cp[1].yv";
connectAttr "solver.out[29]" "LeftMiddleFingerShape.cp[1].zv";
connectAttr "solver.out[30]" "LeftMiddleFingerShape.cp[2].xv";
connectAttr "solver.out[31]" "LeftMiddleFingerShape.cp[2].yv";
connectAttr "solver.out[32]" "LeftMiddleFingerShape.cp[2].zv";
connectAttr "solver.out[33]" "LeftMiddleFingerShape.cp[3].xv";
connectAttr "solver.out[34]" "LeftMiddleFingerShape.cp[3].yv";
connectAttr "solver.out[35]" "LeftMiddleFingerShape.cp[3].zv";
connectAttr "solver.out[12]" "LeftIndexFingerShape.cp[0].xv";
connectAttr "solver.out[13]" "LeftIndexFingerShape.cp[0].yv";
connectAttr "solver.out[14]" "LeftIndexFingerShape.cp[0].zv";
connectAttr "solver.out[15]" "LeftIndexFingerShape.cp[1].xv";
connectAttr "solver.out[16]" "LeftIndexFingerShape.cp[1].yv";
connectAttr "solver.out[17]" "LeftIndexFingerShape.cp[1].zv";
connectAttr "solver.out[18]" "LeftIndexFingerShape.cp[2].xv";
connectAttr "solver.out[19]" "LeftIndexFingerShape.cp[2].yv";
connectAttr "solver.out[20]" "LeftIndexFingerShape.cp[2].zv";
connectAttr "solver.out[21]" "LeftIndexFingerShape.cp[3].xv";
connectAttr "solver.out[22]" "LeftIndexFingerShape.cp[3].yv";
connectAttr "solver.out[23]" "LeftIndexFingerShape.cp[3].zv";
connectAttr "solver.out[0]" "LeftThumbShape.cp[0].xv";
connectAttr "solver.out[1]" "LeftThumbShape.cp[0].yv";
connectAttr "solver.out[2]" "LeftThumbShape.cp[0].zv";
connectAttr "solver.out[3]" "LeftThumbShape.cp[1].xv";
connectAttr "solver.out[4]" "LeftThumbShape.cp[1].yv";
connectAttr "solver.out[5]" "LeftThumbShape.cp[1].zv";
connectAttr "solver.out[6]" "LeftThumbShape.cp[2].xv";
connectAttr "solver.out[7]" "LeftThumbShape.cp[2].yv";
connectAttr "solver.out[8]" "LeftThumbShape.cp[2].zv";
connectAttr "solver.out[9]" "LeftThumbShape.cp[3].xv";
connectAttr "solver.out[10]" "LeftThumbShape.cp[3].yv";
connectAttr "solver.out[11]" "LeftThumbShape.cp[3].zv";
connectAttr "solver.out[60]" "LeftCollarShape.cp[0].xv";
connectAttr "solver.out[61]" "LeftCollarShape.cp[0].yv";
connectAttr "solver.out[62]" "LeftCollarShape.cp[0].zv";
connectAttr "solver.out[63]" "LeftCollarShape.cp[1].xv";
connectAttr "solver.out[64]" "LeftCollarShape.cp[1].yv";
connectAttr "solver.out[65]" "LeftCollarShape.cp[1].zv";
connectAttr "solver.out[135]" "RightCollarShape.cp[0].xv";
connectAttr "solver.out[136]" "RightCollarShape.cp[0].yv";
connectAttr "solver.out[137]" "RightCollarShape.cp[0].zv";
connectAttr "solver.out[138]" "RightCollarShape.cp[1].xv";
connectAttr "solver.out[139]" "RightCollarShape.cp[1].yv";
connectAttr "solver.out[140]" "RightCollarShape.cp[1].zv";
connectAttr "solver.out[66]" "LeftArmShape.cp[0].xv";
connectAttr "solver.out[67]" "LeftArmShape.cp[0].yv";
connectAttr "solver.out[68]" "LeftArmShape.cp[0].zv";
connectAttr "solver.out[69]" "LeftArmShape.cp[1].xv";
connectAttr "solver.out[70]" "LeftArmShape.cp[1].yv";
connectAttr "solver.out[71]" "LeftArmShape.cp[1].zv";
connectAttr "solver.out[72]" "LeftArmShape.cp[2].xv";
connectAttr "solver.out[73]" "LeftArmShape.cp[2].yv";
connectAttr "solver.out[74]" "LeftArmShape.cp[2].zv";
connectAttr "solver.out[141]" "RightArmShape.cp[0].xv";
connectAttr "solver.out[142]" "RightArmShape.cp[0].yv";
connectAttr "solver.out[143]" "RightArmShape.cp[0].zv";
connectAttr "solver.out[144]" "RightArmShape.cp[1].xv";
connectAttr "solver.out[145]" "RightArmShape.cp[1].yv";
connectAttr "solver.out[146]" "RightArmShape.cp[1].zv";
connectAttr "solver.out[147]" "RightArmShape.cp[2].xv";
connectAttr "solver.out[148]" "RightArmShape.cp[2].yv";
connectAttr "solver.out[149]" "RightArmShape.cp[2].zv";
connectAttr "solver.out[180]" "SpineShape.cp[0].xv";
connectAttr "solver.out[181]" "SpineShape.cp[0].yv";
connectAttr "solver.out[182]" "SpineShape.cp[0].zv";
connectAttr "solver.out[183]" "SpineShape.cp[1].xv";
connectAttr "solver.out[184]" "SpineShape.cp[1].yv";
connectAttr "solver.out[185]" "SpineShape.cp[1].zv";
connectAttr "solver.out[186]" "SpineShape.cp[2].xv";
connectAttr "solver.out[187]" "SpineShape.cp[2].yv";
connectAttr "solver.out[188]" "SpineShape.cp[2].zv";
connectAttr "solver.out[189]" "SpineShape.cp[3].xv";
connectAttr "solver.out[190]" "SpineShape.cp[3].yv";
connectAttr "solver.out[191]" "SpineShape.cp[3].zv";
connectAttr "solver.out[192]" "SpineShape.cp[4].xv";
connectAttr "solver.out[193]" "SpineShape.cp[4].yv";
connectAttr "solver.out[194]" "SpineShape.cp[4].zv";
connectAttr "solver.out[195]" "SpineShape.cp[5].xv";
connectAttr "solver.out[196]" "SpineShape.cp[5].yv";
connectAttr "solver.out[197]" "SpineShape.cp[5].zv";
connectAttr "Lf_leg_fk1_opm.o" "Lf_leg_fk1_ctrl.opm";
connectAttr "Lf_leg_fk2_opm.o" "Lf_leg_fk2_ctrl.opm";
connectAttr "Lf_leg_fk3_opm.o" "Lf_leg_fk3_ctrl.opm";
connectAttr "Lf_leg_pv_opm.o" "Lf_leg_pv_ctrl.opm";
connectAttr "Lf_leg_ik_opm.o" "Lf_leg_ik_ctrl.opm";
connectAttr "Rt_finger_index_1_opm.o" "Rt_finger_index_1_ctrl.opm";
connectAttr "Rt_finger_index_2_opm.o" "Rt_finger_index_2_ctrl.opm";
connectAttr "Rt_finger_index_3_opm.o" "Rt_finger_index_3_ctrl.opm";
connectAttr "Rt_finger_mid_1_opm.o" "Rt_finger_mid_1_ctrl.opm";
connectAttr "Rt_finger_mid_2_opm.o" "Rt_finger_mid_2_ctrl.opm";
connectAttr "Rt_finger_mid_3_opm.o" "Rt_finger_mid_3_ctrl.opm";
connectAttr "Rt_finger_ring_1_opm.o" "Rt_finger_ring_1_ctrl.opm";
connectAttr "Rt_finger_ring_2_opm.o" "Rt_finger_ring_2_ctrl.opm";
connectAttr "Rt_finger_ring_3_opm.o" "Rt_finger_ring_3_ctrl.opm";
connectAttr "Rt_finger_pinky_1_opm.o" "Rt_finger_pinky_1_ctrl.opm";
connectAttr "Rt_finger_pinky_2_opm.o" "Rt_finger_pinky_2_ctrl.opm";
connectAttr "Rt_finger_pinky_3_opm.o" "Rt_finger_pinky_3_ctrl.opm";
connectAttr "Rt_finger_thumb_1_opm.o" "Rt_finger_thumb_1_ctrl.opm";
connectAttr "Rt_finger_thumb_2_opm.o" "Rt_finger_thumb_2_ctrl.opm";
connectAttr "Rt_finger_thumb_3_opm.o" "Rt_finger_thumb_3_ctrl.opm";
connectAttr "Lf_finger_index_1_opm.o" "Lf_finger_index_1_ctrl.opm";
connectAttr "Lf_finger_index_2_opm.o" "Lf_finger_index_2_ctrl.opm";
connectAttr "Lf_finger_index_3_opm.o" "Lf_finger_index_3_ctrl.opm";
connectAttr "Lf_finger_mid_1_opm.o" "Lf_finger_mid_1_ctrl.opm";
connectAttr "Lf_finger_mid_2_opm.o" "Lf_finger_mid_2_ctrl.opm";
connectAttr "Lf_finger_mid_3_opm.o" "Lf_finger_mid_3_ctrl.opm";
connectAttr "Lf_finger_ring_1_opm.o" "Lf_finger_ring_1_ctrl.opm";
connectAttr "Lf_finger_ring_2_opm.o" "Lf_finger_ring_2_ctrl.opm";
connectAttr "Lf_finger_ring_3_opm.o" "Lf_finger_ring_3_ctrl.opm";
connectAttr "Lf_finger_pinky_1_opm.o" "Lf_finger_pinky_1_ctrl.opm";
connectAttr "Lf_finger_pinky_2_opm.o" "Lf_finger_pinky_2_ctrl.opm";
connectAttr "Lf_finger_pinky_3_opm.o" "Lf_finger_pinky_3_ctrl.opm";
connectAttr "Lf_finger_thumb_1_opm.o" "Lf_finger_thumb_1_ctrl.opm";
connectAttr "Lf_finger_thumb_2_opm.o" "Lf_finger_thumb_2_ctrl.opm";
connectAttr "Lf_finger_thumb_3_opm.o" "Lf_finger_thumb_3_ctrl.opm";
connectAttr "spine_hips_opm.o" "spine_hips_ctrl.opm";
connectAttr "Lf_arm_fk1_opm.o" "Lf_arm_fk1_ctrl.opm";
connectAttr "Lf_arm_fk2_opm.o" "Lf_arm_fk2_ctrl.opm";
connectAttr "Lf_arm_fk3_opm.o" "Lf_arm_fk3_ctrl.opm";
connectAttr "Lf_arm_pv_opm.o" "Lf_arm_pv_ctrl.opm";
connectAttr "Lf_arm_ik_opm.o" "Lf_arm_ik_ctrl.opm";
connectAttr "Rt_arm_fk1_opm.o" "Rt_arm_fk1_ctrl.opm";
connectAttr "Rt_arm_fk2_opm.o" "Rt_arm_fk2_ctrl.opm";
connectAttr "Rt_arm_fk3_opm.o" "Rt_arm_fk3_ctrl.opm";
connectAttr "Rt_arm_pv_opm.o" "Rt_arm_pv_ctrl.opm";
connectAttr "Rt_arm_ik_opm.o" "Rt_arm_ik_ctrl.opm";
connectAttr "Rt_leg_fk1_opm.o" "Rt_leg_fk1_ctrl.opm";
connectAttr "Rt_leg_fk2_opm.o" "Rt_leg_fk2_ctrl.opm";
connectAttr "Rt_leg_fk3_opm.o" "Rt_leg_fk3_ctrl.opm";
connectAttr "Rt_leg_pv_opm.o" "Rt_leg_pv_ctrl.opm";
connectAttr "Rt_leg_ik_opm.o" "Rt_leg_ik_ctrl.opm";
connectAttr "spine_chest_opm.o" "spine_chest_ctrl.opm";
connectAttr "Rt_arm_clav_opm.o" "Rt_arm_clav_ctrl.opm";
connectAttr "Lf_arm_clav_opm.o" "Lf_arm_clav_ctrl.opm";
connectAttr "root_opm.o" "root_ctrl.opm";
connectAttr "head_opm.o" "head_ctrl.opm";
connectAttr "retarget.RightPinkyFinger1" "RightPinkyFinger1.im";
connectAttr "solver.out[654]" "Rt_finger_pinky_1_opm.i00";
connectAttr "solver.out[655]" "Rt_finger_pinky_1_opm.i01";
connectAttr "solver.out[656]" "Rt_finger_pinky_1_opm.i02";
connectAttr "solver.out[657]" "Rt_finger_pinky_1_opm.i10";
connectAttr "solver.out[658]" "Rt_finger_pinky_1_opm.i11";
connectAttr "solver.out[659]" "Rt_finger_pinky_1_opm.i12";
connectAttr "solver.out[660]" "Rt_finger_pinky_1_opm.i20";
connectAttr "solver.out[661]" "Rt_finger_pinky_1_opm.i21";
connectAttr "solver.out[662]" "Rt_finger_pinky_1_opm.i22";
connectAttr "solver.out[663]" "Rt_finger_pinky_1_opm.i30";
connectAttr "solver.out[664]" "Rt_finger_pinky_1_opm.i31";
connectAttr "solver.out[665]" "Rt_finger_pinky_1_opm.i32";
connectAttr "solver.out[606]" "Rt_finger_mid_1_opm.i00";
connectAttr "solver.out[607]" "Rt_finger_mid_1_opm.i01";
connectAttr "solver.out[608]" "Rt_finger_mid_1_opm.i02";
connectAttr "solver.out[609]" "Rt_finger_mid_1_opm.i10";
connectAttr "solver.out[610]" "Rt_finger_mid_1_opm.i11";
connectAttr "solver.out[611]" "Rt_finger_mid_1_opm.i12";
connectAttr "solver.out[612]" "Rt_finger_mid_1_opm.i20";
connectAttr "solver.out[613]" "Rt_finger_mid_1_opm.i21";
connectAttr "solver.out[614]" "Rt_finger_mid_1_opm.i22";
connectAttr "solver.out[615]" "Rt_finger_mid_1_opm.i30";
connectAttr "solver.out[616]" "Rt_finger_mid_1_opm.i31";
connectAttr "solver.out[617]" "Rt_finger_mid_1_opm.i32";
connectAttr "solver.out[168]" "spine_hips_opm.i00";
connectAttr "solver.out[169]" "spine_hips_opm.i01";
connectAttr "solver.out[170]" "spine_hips_opm.i02";
connectAttr "solver.out[171]" "spine_hips_opm.i10";
connectAttr "solver.out[172]" "spine_hips_opm.i11";
connectAttr "solver.out[173]" "spine_hips_opm.i12";
connectAttr "solver.out[174]" "spine_hips_opm.i20";
connectAttr "solver.out[175]" "spine_hips_opm.i21";
connectAttr "solver.out[176]" "spine_hips_opm.i22";
connectAttr "solver.out[177]" "spine_hips_opm.i30";
connectAttr "solver.out[178]" "spine_hips_opm.i31";
connectAttr "solver.out[179]" "spine_hips_opm.i32";
connectAttr "solver.out[570]" "Rt_finger_thumb_2_opm.i00";
connectAttr "solver.out[571]" "Rt_finger_thumb_2_opm.i01";
connectAttr "solver.out[572]" "Rt_finger_thumb_2_opm.i02";
connectAttr "solver.out[573]" "Rt_finger_thumb_2_opm.i10";
connectAttr "solver.out[574]" "Rt_finger_thumb_2_opm.i11";
connectAttr "solver.out[575]" "Rt_finger_thumb_2_opm.i12";
connectAttr "solver.out[576]" "Rt_finger_thumb_2_opm.i20";
connectAttr "solver.out[577]" "Rt_finger_thumb_2_opm.i21";
connectAttr "solver.out[578]" "Rt_finger_thumb_2_opm.i22";
connectAttr "solver.out[579]" "Rt_finger_thumb_2_opm.i30";
connectAttr "solver.out[580]" "Rt_finger_thumb_2_opm.i31";
connectAttr "solver.out[581]" "Rt_finger_thumb_2_opm.i32";
connectAttr "solver.out[618]" "Rt_finger_mid_2_opm.i00";
connectAttr "solver.out[619]" "Rt_finger_mid_2_opm.i01";
connectAttr "solver.out[620]" "Rt_finger_mid_2_opm.i02";
connectAttr "solver.out[621]" "Rt_finger_mid_2_opm.i10";
connectAttr "solver.out[622]" "Rt_finger_mid_2_opm.i11";
connectAttr "solver.out[623]" "Rt_finger_mid_2_opm.i12";
connectAttr "solver.out[624]" "Rt_finger_mid_2_opm.i20";
connectAttr "solver.out[625]" "Rt_finger_mid_2_opm.i21";
connectAttr "solver.out[626]" "Rt_finger_mid_2_opm.i22";
connectAttr "solver.out[627]" "Rt_finger_mid_2_opm.i30";
connectAttr "solver.out[628]" "Rt_finger_mid_2_opm.i31";
connectAttr "solver.out[629]" "Rt_finger_mid_2_opm.i32";
connectAttr "clip.SpineX" "solver.in[0]";
connectAttr "clip.SpineY" "solver.in[1]";
connectAttr "clip.SpineZ" "solver.in[2]";
connectAttr "clip.NeckX" "solver.in[3]";
connectAttr "clip.NeckY" "solver.in[4]";
connectAttr "clip.NeckZ" "solver.in[5]";
connectAttr "clip.HeadX" "solver.in[6]";
connectAttr "clip.HeadY" "solver.in[7]";
connectAttr "clip.HeadZ" "solver.in[8]";
connectAttr "clip.Head_ZX" "solver.in[9]";
connectAttr "clip.Head_ZY" "solver.in[10]";
connectAttr "clip.Head_ZZ" "solver.in[11]";
connectAttr "clip.Spine_ZX" "solver.in[12]";
connectAttr "clip.Spine_ZY" "solver.in[13]";
connectAttr "clip.Spine_ZZ" "solver.in[14]";
connectAttr "clip.Hip_ZX" "solver.in[15]";
connectAttr "clip.Hip_ZY" "solver.in[16]";
connectAttr "clip.Hip_ZZ" "solver.in[17]";
connectAttr "clip.LeftHipX" "solver.in[18]";
connectAttr "clip.LeftHipY" "solver.in[19]";
connectAttr "clip.LeftHipZ" "solver.in[20]";
connectAttr "clip.LeftKneeX" "solver.in[21]";
connectAttr "clip.LeftKneeY" "solver.in[22]";
connectAttr "clip.LeftKneeZ" "solver.in[23]";
connectAttr "clip.LeftFootX" "solver.in[24]";
connectAttr "clip.LeftFootY" "solver.in[25]";
connectAttr "clip.LeftFootZ" "solver.in[26]";
connectAttr "clip.LeftToeX" "solver.in[27]";
connectAttr "clip.LeftToeY" "solver.in[28]";
connectAttr "clip.LeftToeZ" "solver.in[29]";
connectAttr "clip.LeftCollarX" "solver.in[30]";
connectAttr "clip.LeftCollarY" "solver.in[31]";
connectAttr "clip.LeftCollarZ" "solver.in[32]";
connectAttr "clip.LeftShoulderX" "solver.in[33]";
connectAttr "clip.LeftShoulderY" "solver.in[34]";
connectAttr "clip.LeftShoulderZ" "solver.in[35]";
connectAttr "clip.LeftElbowX" "solver.in[36]";
connectAttr "clip.LeftElbowY" "solver.in[37]";
connectAttr "clip.LeftElbowZ" "solver.in[38]";
connectAttr "clip.LeftHandX" "solver.in[39]";
connectAttr "clip.LeftHandY" "solver.in[40]";
connectAttr "clip.LeftHandZ" "solver.in[41]";
connectAttr "clip.LeftBigToeX" "solver.in[42]";
connectAttr "clip.LeftBigToeY" "solver.in[43]";
connectAttr "clip.LeftBigToeZ" "solver.in[44]";
connectAttr "clip.LeftIndexToeX" "solver.in[45]";
connectAttr "clip.LeftIndexToeY" "solver.in[46]";
connectAttr "clip.LeftIndexToeZ" "solver.in[47]";
connectAttr "clip.LeftMiddleToeX" "solver.in[48]";
connectAttr "clip.LeftMiddleToeY" "solver.in[49]";
connectAttr "clip.LeftMiddleToeZ" "solver.in[50]";
connectAttr "clip.LeftRingToeX" "solver.in[51]";
connectAttr "clip.LeftRingToeY" "solver.in[52]";
connectAttr "clip.LeftRingToeZ" "solver.in[53]";
connectAttr "clip.LeftPinkyToeX" "solver.in[54]";
connectAttr "clip.LeftPinkyToeY" "solver.in[55]";
connectAttr "clip.LeftPinkyToeZ" "solver.in[56]";
connectAttr "clip.LeftCollar_ZX" "solver.in[57]";
connectAttr "clip.LeftCollar_ZY" "solver.in[58]";
connectAttr "clip.LeftCollar_ZZ" "solver.in[59]";
connectAttr "clip.LeftHand_ZX" "solver.in[60]";
connectAttr "clip.LeftHand_ZY" "solver.in[61]";
connectAttr "clip.LeftHand_ZZ" "solver.in[62]";
connectAttr "clip.LeftToe_XX" "solver.in[63]";
connectAttr "clip.LeftToe_XY" "solver.in[64]";
connectAttr "clip.LeftToe_XZ" "solver.in[65]";
connectAttr "clip.LeftToe_YX" "solver.in[66]";
connectAttr "clip.LeftToe_YY" "solver.in[67]";
connectAttr "clip.LeftToe_YZ" "solver.in[68]";
connectAttr "clip.LeftThumbX" "solver.in[69]";
connectAttr "clip.LeftThumbY" "solver.in[70]";
connectAttr "clip.LeftThumbZ" "solver.in[71]";
connectAttr "clip.LeftThumb1X" "solver.in[72]";
connectAttr "clip.LeftThumb1Y" "solver.in[73]";
connectAttr "clip.LeftThumb1Z" "solver.in[74]";
connectAttr "clip.LeftThumb2X" "solver.in[75]";
connectAttr "clip.LeftThumb2Y" "solver.in[76]";
connectAttr "clip.LeftThumb2Z" "solver.in[77]";
connectAttr "clip.LeftIndexFingerX" "solver.in[78]";
connectAttr "clip.LeftIndexFingerY" "solver.in[79]";
connectAttr "clip.LeftIndexFingerZ" "solver.in[80]";
connectAttr "clip.LeftIndexFinger1X" "solver.in[81]";
connectAttr "clip.LeftIndexFinger1Y" "solver.in[82]";
connectAttr "clip.LeftIndexFinger1Z" "solver.in[83]";
connectAttr "clip.LeftIndexFinger2X" "solver.in[84]";
connectAttr "clip.LeftIndexFinger2Y" "solver.in[85]";
connectAttr "clip.LeftIndexFinger2Z" "solver.in[86]";
connectAttr "clip.LeftMiddleFingerX" "solver.in[87]";
connectAttr "clip.LeftMiddleFingerY" "solver.in[88]";
connectAttr "clip.LeftMiddleFingerZ" "solver.in[89]";
connectAttr "clip.LeftMiddleFinger1X" "solver.in[90]";
connectAttr "clip.LeftMiddleFinger1Y" "solver.in[91]";
connectAttr "clip.LeftMiddleFinger1Z" "solver.in[92]";
connectAttr "clip.LeftMiddleFinger2X" "solver.in[93]";
connectAttr "clip.LeftMiddleFinger2Y" "solver.in[94]";
connectAttr "clip.LeftMiddleFinger2Z" "solver.in[95]";
connectAttr "clip.LeftRingFingerX" "solver.in[96]";
connectAttr "clip.LeftRingFingerY" "solver.in[97]";
connectAttr "clip.LeftRingFingerZ" "solver.in[98]";
connectAttr "clip.LeftRingFinger1X" "solver.in[99]";
connectAttr "clip.LeftRingFinger1Y" "solver.in[100]";
connectAttr "clip.LeftRingFinger1Z" "solver.in[101]";
connectAttr "clip.LeftRingFinger2X" "solver.in[102]";
connectAttr "clip.LeftRingFinger2Y" "solver.in[103]";
connectAttr "clip.LeftRingFinger2Z" "solver.in[104]";
connectAttr "clip.LeftPinkyFingerX" "solver.in[105]";
connectAttr "clip.LeftPinkyFingerY" "solver.in[106]";
connectAttr "clip.LeftPinkyFingerZ" "solver.in[107]";
connectAttr "clip.LeftPinkyFinger1X" "solver.in[108]";
connectAttr "clip.LeftPinkyFinger1Y" "solver.in[109]";
connectAttr "clip.LeftPinkyFinger1Z" "solver.in[110]";
connectAttr "clip.LeftPinkyFinger2X" "solver.in[111]";
connectAttr "clip.LeftPinkyFinger2Y" "solver.in[112]";
connectAttr "clip.LeftPinkyFinger2Z" "solver.in[113]";
connectAttr "clip.RightHipX" "solver.in[114]";
connectAttr "clip.RightHipY" "solver.in[115]";
connectAttr "clip.RightHipZ" "solver.in[116]";
connectAttr "clip.RightKneeX" "solver.in[117]";
connectAttr "clip.RightKneeY" "solver.in[118]";
connectAttr "clip.RightKneeZ" "solver.in[119]";
connectAttr "clip.RightFootX" "solver.in[120]";
connectAttr "clip.RightFootY" "solver.in[121]";
connectAttr "clip.RightFootZ" "solver.in[122]";
connectAttr "clip.RightToeX" "solver.in[123]";
connectAttr "clip.RightToeY" "solver.in[124]";
connectAttr "clip.RightToeZ" "solver.in[125]";
connectAttr "clip.RightCollarX" "solver.in[126]";
connectAttr "clip.RightCollarY" "solver.in[127]";
connectAttr "clip.RightCollarZ" "solver.in[128]";
connectAttr "clip.RightShoulderX" "solver.in[129]";
connectAttr "clip.RightShoulderY" "solver.in[130]";
connectAttr "clip.RightShoulderZ" "solver.in[131]";
connectAttr "clip.RightElbowX" "solver.in[132]";
connectAttr "clip.RightElbowY" "solver.in[133]";
connectAttr "clip.RightElbowZ" "solver.in[134]";
connectAttr "clip.RightHandX" "solver.in[135]";
connectAttr "clip.RightHandY" "solver.in[136]";
connectAttr "clip.RightHandZ" "solver.in[137]";
connectAttr "clip.RightBigToeX" "solver.in[138]";
connectAttr "clip.RightBigToeY" "solver.in[139]";
connectAttr "clip.RightBigToeZ" "solver.in[140]";
connectAttr "clip.RightIndexToeX" "solver.in[141]";
connectAttr "clip.RightIndexToeY" "solver.in[142]";
connectAttr "clip.RightIndexToeZ" "solver.in[143]";
connectAttr "clip.RightMiddleToeX" "solver.in[144]";
connectAttr "clip.RightMiddleToeY" "solver.in[145]";
connectAttr "clip.RightMiddleToeZ" "solver.in[146]";
connectAttr "clip.RightRingToeX" "solver.in[147]";
connectAttr "clip.RightRingToeY" "solver.in[148]";
connectAttr "clip.RightRingToeZ" "solver.in[149]";
connectAttr "clip.RightPinkyToeX" "solver.in[150]";
connectAttr "clip.RightPinkyToeY" "solver.in[151]";
connectAttr "clip.RightPinkyToeZ" "solver.in[152]";
connectAttr "clip.RightCollar_ZX" "solver.in[153]";
connectAttr "clip.RightCollar_ZY" "solver.in[154]";
connectAttr "clip.RightCollar_ZZ" "solver.in[155]";
connectAttr "clip.RightHand_ZX" "solver.in[156]";
connectAttr "clip.RightHand_ZY" "solver.in[157]";
connectAttr "clip.RightHand_ZZ" "solver.in[158]";
connectAttr "clip.RightToe_XX" "solver.in[159]";
connectAttr "clip.RightToe_XY" "solver.in[160]";
connectAttr "clip.RightToe_XZ" "solver.in[161]";
connectAttr "clip.RightToe_YX" "solver.in[162]";
connectAttr "clip.RightToe_YY" "solver.in[163]";
connectAttr "clip.RightToe_YZ" "solver.in[164]";
connectAttr "clip.RightThumbX" "solver.in[165]";
connectAttr "clip.RightThumbY" "solver.in[166]";
connectAttr "clip.RightThumbZ" "solver.in[167]";
connectAttr "clip.RightThumb1X" "solver.in[168]";
connectAttr "clip.RightThumb1Y" "solver.in[169]";
connectAttr "clip.RightThumb1Z" "solver.in[170]";
connectAttr "clip.RightThumb2X" "solver.in[171]";
connectAttr "clip.RightThumb2Y" "solver.in[172]";
connectAttr "clip.RightThumb2Z" "solver.in[173]";
connectAttr "clip.RightIndexFingerX" "solver.in[174]";
connectAttr "clip.RightIndexFingerY" "solver.in[175]";
connectAttr "clip.RightIndexFingerZ" "solver.in[176]";
connectAttr "clip.RightIndexFinger1X" "solver.in[177]";
connectAttr "clip.RightIndexFinger1Y" "solver.in[178]";
connectAttr "clip.RightIndexFinger1Z" "solver.in[179]";
connectAttr "clip.RightIndexFinger2X" "solver.in[180]";
connectAttr "clip.RightIndexFinger2Y" "solver.in[181]";
connectAttr "clip.RightIndexFinger2Z" "solver.in[182]";
connectAttr "clip.RightMiddleFingerX" "solver.in[183]";
connectAttr "clip.RightMiddleFingerY" "solver.in[184]";
connectAttr "clip.RightMiddleFingerZ" "solver.in[185]";
connectAttr "clip.RightMiddleFinger1X" "solver.in[186]";
connectAttr "clip.RightMiddleFinger1Y" "solver.in[187]";
connectAttr "clip.RightMiddleFinger1Z" "solver.in[188]";
connectAttr "clip.RightMiddleFinger2X" "solver.in[189]";
connectAttr "clip.RightMiddleFinger2Y" "solver.in[190]";
connectAttr "clip.RightMiddleFinger2Z" "solver.in[191]";
connectAttr "clip.RightRingFingerX" "solver.in[192]";
connectAttr "clip.RightRingFingerY" "solver.in[193]";
connectAttr "clip.RightRingFingerZ" "solver.in[194]";
connectAttr "clip.RightRingFinger1X" "solver.in[195]";
connectAttr "clip.RightRingFinger1Y" "solver.in[196]";
connectAttr "clip.RightRingFinger1Z" "solver.in[197]";
connectAttr "clip.RightRingFinger2X" "solver.in[198]";
connectAttr "clip.RightRingFinger2Y" "solver.in[199]";
connectAttr "clip.RightRingFinger2Z" "solver.in[200]";
connectAttr "clip.RightPinkyFingerX" "solver.in[201]";
connectAttr "clip.RightPinkyFingerY" "solver.in[202]";
connectAttr "clip.RightPinkyFingerZ" "solver.in[203]";
connectAttr "clip.RightPinkyFinger1X" "solver.in[204]";
connectAttr "clip.RightPinkyFinger1Y" "solver.in[205]";
connectAttr "clip.RightPinkyFinger1Z" "solver.in[206]";
connectAttr "clip.RightPinkyFinger2X" "solver.in[207]";
connectAttr "clip.RightPinkyFinger2Y" "solver.in[208]";
connectAttr "clip.RightPinkyFinger2Z" "solver.in[209]";
connectAttr "clip.chest_pivot_negX" "solver.in[210]";
connectAttr "clip.chest_pivot_negY" "solver.in[211]";
connectAttr "clip.chest_pivot_negZ" "solver.in[212]";
connectAttr "clip.chest_pivot_posX" "solver.in[213]";
connectAttr "clip.chest_pivot_posY" "solver.in[214]";
connectAttr "clip.chest_pivot_posZ" "solver.in[215]";
connectAttr "clip.hips_pivot_negX" "solver.in[216]";
connectAttr "clip.hips_pivot_negY" "solver.in[217]";
connectAttr "clip.hips_pivot_negZ" "solver.in[218]";
connectAttr "clip.hips_pivot_posX" "solver.in[219]";
connectAttr "clip.hips_pivot_posY" "solver.in[220]";
connectAttr "clip.hips_pivot_posZ" "solver.in[221]";
connectAttr "clip.thigh_length" "solver.in[222]";
connectAttr "clip.shin_length" "solver.in[223]";
connectAttr "clip.hip_width" "solver.in[224]";
connectAttr "clip.spine0_length" "solver.in[225]";
connectAttr "clip.spine1_length" "solver.in[226]";
connectAttr "clip.spine2_length" "solver.in[227]";
connectAttr "clip.spine3_length" "solver.in[228]";
connectAttr "clip.spine4_length" "solver.in[229]";
connectAttr "retarget.foot_lock_tolerance" "solver.in[230]";
connectAttr "clip.hip_pivot" "solver.in[231]";
connectAttr "clip.chest_pivot" "solver.in[232]";
connectAttr "retarget.foot_offset" "solver.in[233]";
connectAttr "retarget.clav_offset" "solver.in[234]";
connectAttr "retarget.hand_orientation" "solver.in[235]";
connectAttr "solver.out[522]" "Lf_finger_ring_2_opm.i00";
connectAttr "solver.out[523]" "Lf_finger_ring_2_opm.i01";
connectAttr "solver.out[524]" "Lf_finger_ring_2_opm.i02";
connectAttr "solver.out[525]" "Lf_finger_ring_2_opm.i10";
connectAttr "solver.out[526]" "Lf_finger_ring_2_opm.i11";
connectAttr "solver.out[527]" "Lf_finger_ring_2_opm.i12";
connectAttr "solver.out[528]" "Lf_finger_ring_2_opm.i20";
connectAttr "solver.out[529]" "Lf_finger_ring_2_opm.i21";
connectAttr "solver.out[530]" "Lf_finger_ring_2_opm.i22";
connectAttr "solver.out[531]" "Lf_finger_ring_2_opm.i30";
connectAttr "solver.out[532]" "Lf_finger_ring_2_opm.i31";
connectAttr "solver.out[533]" "Lf_finger_ring_2_opm.i32";
connectAttr "solver.out[378]" "Lf_arm_fk3_opm.i00";
connectAttr "solver.out[379]" "Lf_arm_fk3_opm.i01";
connectAttr "solver.out[380]" "Lf_arm_fk3_opm.i02";
connectAttr "solver.out[381]" "Lf_arm_fk3_opm.i10";
connectAttr "solver.out[382]" "Lf_arm_fk3_opm.i11";
connectAttr "solver.out[383]" "Lf_arm_fk3_opm.i12";
connectAttr "solver.out[384]" "Lf_arm_fk3_opm.i20";
connectAttr "solver.out[385]" "Lf_arm_fk3_opm.i21";
connectAttr "solver.out[386]" "Lf_arm_fk3_opm.i22";
connectAttr "solver.out[387]" "Lf_arm_fk3_opm.i30";
connectAttr "solver.out[388]" "Lf_arm_fk3_opm.i31";
connectAttr "solver.out[389]" "Lf_arm_fk3_opm.i32";
connectAttr "retarget.RightRingFinger1" "RightRingFinger1.im";
connectAttr "retarget.RightRingFinger2" "RightRingFinger2.im";
connectAttr "solver.out[438]" "Lf_finger_thumb_1_opm.i00";
connectAttr "solver.out[439]" "Lf_finger_thumb_1_opm.i01";
connectAttr "solver.out[440]" "Lf_finger_thumb_1_opm.i02";
connectAttr "solver.out[441]" "Lf_finger_thumb_1_opm.i10";
connectAttr "solver.out[442]" "Lf_finger_thumb_1_opm.i11";
connectAttr "solver.out[443]" "Lf_finger_thumb_1_opm.i12";
connectAttr "solver.out[444]" "Lf_finger_thumb_1_opm.i20";
connectAttr "solver.out[445]" "Lf_finger_thumb_1_opm.i21";
connectAttr "solver.out[446]" "Lf_finger_thumb_1_opm.i22";
connectAttr "solver.out[447]" "Lf_finger_thumb_1_opm.i30";
connectAttr "solver.out[448]" "Lf_finger_thumb_1_opm.i31";
connectAttr "solver.out[449]" "Lf_finger_thumb_1_opm.i32";
connectAttr "retarget.LeftRingFinger_Z" "LeftRingFinger_Z.im";
connectAttr "solver.out[228]" "Lf_leg_fk1_opm.i00";
connectAttr "solver.out[229]" "Lf_leg_fk1_opm.i01";
connectAttr "solver.out[230]" "Lf_leg_fk1_opm.i02";
connectAttr "solver.out[231]" "Lf_leg_fk1_opm.i10";
connectAttr "solver.out[232]" "Lf_leg_fk1_opm.i11";
connectAttr "solver.out[233]" "Lf_leg_fk1_opm.i12";
connectAttr "solver.out[234]" "Lf_leg_fk1_opm.i20";
connectAttr "solver.out[235]" "Lf_leg_fk1_opm.i21";
connectAttr "solver.out[236]" "Lf_leg_fk1_opm.i22";
connectAttr "solver.out[237]" "Lf_leg_fk1_opm.i30";
connectAttr "solver.out[238]" "Lf_leg_fk1_opm.i31";
connectAttr "solver.out[239]" "Lf_leg_fk1_opm.i32";
connectAttr "solver.out[198]" "spine_chest_opm.i00";
connectAttr "solver.out[199]" "spine_chest_opm.i01";
connectAttr "solver.out[200]" "spine_chest_opm.i02";
connectAttr "solver.out[201]" "spine_chest_opm.i10";
connectAttr "solver.out[202]" "spine_chest_opm.i11";
connectAttr "solver.out[203]" "spine_chest_opm.i12";
connectAttr "solver.out[204]" "spine_chest_opm.i20";
connectAttr "solver.out[205]" "spine_chest_opm.i21";
connectAttr "solver.out[206]" "spine_chest_opm.i22";
connectAttr "solver.out[207]" "spine_chest_opm.i30";
connectAttr "solver.out[208]" "spine_chest_opm.i31";
connectAttr "solver.out[209]" "spine_chest_opm.i32";
connectAttr "place2dTexture2.o" "file3.uv";
connectAttr "place2dTexture2.ofu" "file3.ofu";
connectAttr "place2dTexture2.ofv" "file3.ofv";
connectAttr "place2dTexture2.rf" "file3.rf";
connectAttr "place2dTexture2.reu" "file3.reu";
connectAttr "place2dTexture2.rev" "file3.rev";
connectAttr "place2dTexture2.vt1" "file3.vt1";
connectAttr "place2dTexture2.vt2" "file3.vt2";
connectAttr "place2dTexture2.vt3" "file3.vt3";
connectAttr "place2dTexture2.vc1" "file3.vc1";
connectAttr "place2dTexture2.ofs" "file3.fs";
connectAttr ":defaultColorMgtGlobals.cme" "file3.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "file3.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "file3.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "file3.ws";
connectAttr "solver.out[354]" "Lf_arm_fk1_opm.i00";
connectAttr "solver.out[355]" "Lf_arm_fk1_opm.i01";
connectAttr "solver.out[356]" "Lf_arm_fk1_opm.i02";
connectAttr "solver.out[357]" "Lf_arm_fk1_opm.i10";
connectAttr "solver.out[358]" "Lf_arm_fk1_opm.i11";
connectAttr "solver.out[359]" "Lf_arm_fk1_opm.i12";
connectAttr "solver.out[360]" "Lf_arm_fk1_opm.i20";
connectAttr "solver.out[361]" "Lf_arm_fk1_opm.i21";
connectAttr "solver.out[362]" "Lf_arm_fk1_opm.i22";
connectAttr "solver.out[363]" "Lf_arm_fk1_opm.i30";
connectAttr "solver.out[364]" "Lf_arm_fk1_opm.i31";
connectAttr "solver.out[365]" "Lf_arm_fk1_opm.i32";
connectAttr "retarget.LeftThumb_Z" "LeftThumb_Z.im";
connectAttr "retarget.LeftRingFinger2" "LeftRingFinger2.im";
connectAttr "solver.out[264]" "Lf_leg_ik_opm.i00";
connectAttr "solver.out[265]" "Lf_leg_ik_opm.i01";
connectAttr "solver.out[266]" "Lf_leg_ik_opm.i02";
connectAttr "solver.out[267]" "Lf_leg_ik_opm.i10";
connectAttr "solver.out[268]" "Lf_leg_ik_opm.i11";
connectAttr "solver.out[269]" "Lf_leg_ik_opm.i12";
connectAttr "solver.out[270]" "Lf_leg_ik_opm.i20";
connectAttr "solver.out[271]" "Lf_leg_ik_opm.i21";
connectAttr "solver.out[272]" "Lf_leg_ik_opm.i22";
connectAttr "solver.out[273]" "Lf_leg_ik_opm.i30";
connectAttr "solver.out[274]" "Lf_leg_ik_opm.i31";
connectAttr "solver.out[275]" "Lf_leg_ik_opm.i32";
connectAttr "retarget.RightPinkyFinger2" "RightPinkyFinger2.im";
connectAttr "solver.out[414]" "Rt_arm_fk2_opm.i00";
connectAttr "solver.out[415]" "Rt_arm_fk2_opm.i01";
connectAttr "solver.out[416]" "Rt_arm_fk2_opm.i02";
connectAttr "solver.out[417]" "Rt_arm_fk2_opm.i10";
connectAttr "solver.out[418]" "Rt_arm_fk2_opm.i11";
connectAttr "solver.out[419]" "Rt_arm_fk2_opm.i12";
connectAttr "solver.out[420]" "Rt_arm_fk2_opm.i20";
connectAttr "solver.out[421]" "Rt_arm_fk2_opm.i21";
connectAttr "solver.out[422]" "Rt_arm_fk2_opm.i22";
connectAttr "solver.out[423]" "Rt_arm_fk2_opm.i30";
connectAttr "solver.out[424]" "Rt_arm_fk2_opm.i31";
connectAttr "solver.out[425]" "Rt_arm_fk2_opm.i32";
connectAttr "retarget.RightRingFinger_Z" "RightRingFinger_Z.im";
connectAttr "solver.out[510]" "Lf_finger_ring_1_opm.i00";
connectAttr "solver.out[511]" "Lf_finger_ring_1_opm.i01";
connectAttr "solver.out[512]" "Lf_finger_ring_1_opm.i02";
connectAttr "solver.out[513]" "Lf_finger_ring_1_opm.i10";
connectAttr "solver.out[514]" "Lf_finger_ring_1_opm.i11";
connectAttr "solver.out[515]" "Lf_finger_ring_1_opm.i12";
connectAttr "solver.out[516]" "Lf_finger_ring_1_opm.i20";
connectAttr "solver.out[517]" "Lf_finger_ring_1_opm.i21";
connectAttr "solver.out[518]" "Lf_finger_ring_1_opm.i22";
connectAttr "solver.out[519]" "Lf_finger_ring_1_opm.i30";
connectAttr "solver.out[520]" "Lf_finger_ring_1_opm.i31";
connectAttr "solver.out[521]" "Lf_finger_ring_1_opm.i32";
connectAttr "retarget.LeftPinkyFinger2" "LeftPinkyFinger2.im";
connectAttr "solver.out[450]" "Lf_finger_thumb_2_opm.i00";
connectAttr "solver.out[451]" "Lf_finger_thumb_2_opm.i01";
connectAttr "solver.out[452]" "Lf_finger_thumb_2_opm.i02";
connectAttr "solver.out[453]" "Lf_finger_thumb_2_opm.i10";
connectAttr "solver.out[454]" "Lf_finger_thumb_2_opm.i11";
connectAttr "solver.out[455]" "Lf_finger_thumb_2_opm.i12";
connectAttr "solver.out[456]" "Lf_finger_thumb_2_opm.i20";
connectAttr "solver.out[457]" "Lf_finger_thumb_2_opm.i21";
connectAttr "solver.out[458]" "Lf_finger_thumb_2_opm.i22";
connectAttr "solver.out[459]" "Lf_finger_thumb_2_opm.i30";
connectAttr "solver.out[460]" "Lf_finger_thumb_2_opm.i31";
connectAttr "solver.out[461]" "Lf_finger_thumb_2_opm.i32";
connectAttr "solver.out[366]" "Lf_arm_fk2_opm.i00";
connectAttr "solver.out[367]" "Lf_arm_fk2_opm.i01";
connectAttr "solver.out[368]" "Lf_arm_fk2_opm.i02";
connectAttr "solver.out[369]" "Lf_arm_fk2_opm.i10";
connectAttr "solver.out[370]" "Lf_arm_fk2_opm.i11";
connectAttr "solver.out[371]" "Lf_arm_fk2_opm.i12";
connectAttr "solver.out[372]" "Lf_arm_fk2_opm.i20";
connectAttr "solver.out[373]" "Lf_arm_fk2_opm.i21";
connectAttr "solver.out[374]" "Lf_arm_fk2_opm.i22";
connectAttr "solver.out[375]" "Lf_arm_fk2_opm.i30";
connectAttr "solver.out[376]" "Lf_arm_fk2_opm.i31";
connectAttr "solver.out[377]" "Lf_arm_fk2_opm.i32";
connectAttr "retarget.LeftRingFinger" "LeftRingFinger.im";
connectAttr "retarget.LeftThumb2" "LeftThumb2.im";
connectAttr "solver.out[291]" "Rt_leg_fk2_opm.i00";
connectAttr "solver.out[292]" "Rt_leg_fk2_opm.i01";
connectAttr "solver.out[293]" "Rt_leg_fk2_opm.i02";
connectAttr "solver.out[294]" "Rt_leg_fk2_opm.i10";
connectAttr "solver.out[295]" "Rt_leg_fk2_opm.i11";
connectAttr "solver.out[296]" "Rt_leg_fk2_opm.i12";
connectAttr "solver.out[297]" "Rt_leg_fk2_opm.i20";
connectAttr "solver.out[298]" "Rt_leg_fk2_opm.i21";
connectAttr "solver.out[299]" "Rt_leg_fk2_opm.i22";
connectAttr "solver.out[300]" "Rt_leg_fk2_opm.i30";
connectAttr "solver.out[301]" "Rt_leg_fk2_opm.i31";
connectAttr "solver.out[302]" "Rt_leg_fk2_opm.i32";
connectAttr "solver.out[462]" "Lf_finger_index_1_opm.i00";
connectAttr "solver.out[463]" "Lf_finger_index_1_opm.i01";
connectAttr "solver.out[464]" "Lf_finger_index_1_opm.i02";
connectAttr "solver.out[465]" "Lf_finger_index_1_opm.i10";
connectAttr "solver.out[466]" "Lf_finger_index_1_opm.i11";
connectAttr "solver.out[467]" "Lf_finger_index_1_opm.i12";
connectAttr "solver.out[468]" "Lf_finger_index_1_opm.i20";
connectAttr "solver.out[469]" "Lf_finger_index_1_opm.i21";
connectAttr "solver.out[470]" "Lf_finger_index_1_opm.i22";
connectAttr "solver.out[471]" "Lf_finger_index_1_opm.i30";
connectAttr "solver.out[472]" "Lf_finger_index_1_opm.i31";
connectAttr "solver.out[473]" "Lf_finger_index_1_opm.i32";
connectAttr "wood.oc" "pCube1_geo_dup_geoSG.ss";
connectAttr "solver.out[276]" "Lf_leg_pv_opm.i30";
connectAttr "solver.out[277]" "Lf_leg_pv_opm.i31";
connectAttr "solver.out[278]" "Lf_leg_pv_opm.i32";
connectAttr "retarget.LeftIndexFinger_Z" "LeftIndexFinger_Z.im";
connectAttr "retarget.RightThumb2" "RightThumb2.im";
connectAttr "solver.out[315]" "Rt_leg_ik_opm.i00";
connectAttr "solver.out[316]" "Rt_leg_ik_opm.i01";
connectAttr "solver.out[317]" "Rt_leg_ik_opm.i02";
connectAttr "solver.out[318]" "Rt_leg_ik_opm.i10";
connectAttr "solver.out[319]" "Rt_leg_ik_opm.i11";
connectAttr "solver.out[320]" "Rt_leg_ik_opm.i12";
connectAttr "solver.out[321]" "Rt_leg_ik_opm.i20";
connectAttr "solver.out[322]" "Rt_leg_ik_opm.i21";
connectAttr "solver.out[323]" "Rt_leg_ik_opm.i22";
connectAttr "solver.out[324]" "Rt_leg_ik_opm.i30";
connectAttr "solver.out[325]" "Rt_leg_ik_opm.i31";
connectAttr "solver.out[326]" "Rt_leg_ik_opm.i32";
connectAttr "retarget.LeftIndexFinger1" "LeftIndexFinger1.im";
connectAttr "retarget.RightRingFinger" "RightRingFinger.im";
connectAttr "solver.out[498]" "Lf_finger_mid_2_opm.i00";
connectAttr "solver.out[499]" "Lf_finger_mid_2_opm.i01";
connectAttr "solver.out[500]" "Lf_finger_mid_2_opm.i02";
connectAttr "solver.out[501]" "Lf_finger_mid_2_opm.i10";
connectAttr "solver.out[502]" "Lf_finger_mid_2_opm.i11";
connectAttr "solver.out[503]" "Lf_finger_mid_2_opm.i12";
connectAttr "solver.out[504]" "Lf_finger_mid_2_opm.i20";
connectAttr "solver.out[505]" "Lf_finger_mid_2_opm.i21";
connectAttr "solver.out[506]" "Lf_finger_mid_2_opm.i22";
connectAttr "solver.out[507]" "Lf_finger_mid_2_opm.i30";
connectAttr "solver.out[508]" "Lf_finger_mid_2_opm.i31";
connectAttr "solver.out[509]" "Lf_finger_mid_2_opm.i32";
connectAttr "retarget.RightPinkyFinger_Z" "RightPinkyFinger_Z.im";
connectAttr "solver.out[279]" "Rt_leg_fk1_opm.i00";
connectAttr "solver.out[280]" "Rt_leg_fk1_opm.i01";
connectAttr "solver.out[281]" "Rt_leg_fk1_opm.i02";
connectAttr "solver.out[282]" "Rt_leg_fk1_opm.i10";
connectAttr "solver.out[283]" "Rt_leg_fk1_opm.i11";
connectAttr "solver.out[284]" "Rt_leg_fk1_opm.i12";
connectAttr "solver.out[285]" "Rt_leg_fk1_opm.i20";
connectAttr "solver.out[286]" "Rt_leg_fk1_opm.i21";
connectAttr "solver.out[287]" "Rt_leg_fk1_opm.i22";
connectAttr "solver.out[288]" "Rt_leg_fk1_opm.i30";
connectAttr "solver.out[289]" "Rt_leg_fk1_opm.i31";
connectAttr "solver.out[290]" "Rt_leg_fk1_opm.i32";
connectAttr "solver.out[582]" "Rt_finger_index_1_opm.i00";
connectAttr "solver.out[583]" "Rt_finger_index_1_opm.i01";
connectAttr "solver.out[584]" "Rt_finger_index_1_opm.i02";
connectAttr "solver.out[585]" "Rt_finger_index_1_opm.i10";
connectAttr "solver.out[586]" "Rt_finger_index_1_opm.i11";
connectAttr "solver.out[587]" "Rt_finger_index_1_opm.i12";
connectAttr "solver.out[588]" "Rt_finger_index_1_opm.i20";
connectAttr "solver.out[589]" "Rt_finger_index_1_opm.i21";
connectAttr "solver.out[590]" "Rt_finger_index_1_opm.i22";
connectAttr "solver.out[591]" "Rt_finger_index_1_opm.i30";
connectAttr "solver.out[592]" "Rt_finger_index_1_opm.i31";
connectAttr "solver.out[593]" "Rt_finger_index_1_opm.i32";
connectAttr "retarget.LeftPinkyFinger" "LeftPinkyFinger.im";
connectAttr "retarget.RightIndexFinger1" "RightIndexFinger1.im";
connectAttr "retarget.RightThumb" "RightThumb.im";
connectAttr "retarget.RightMiddleFinger_Z" "RightMiddleFinger_Z.im";
connectAttr "retarget.RightMiddleFinger2" "RightMiddleFinger2.im";
connectAttr "solver.out[402]" "Rt_arm_fk1_opm.i00";
connectAttr "solver.out[403]" "Rt_arm_fk1_opm.i01";
connectAttr "solver.out[404]" "Rt_arm_fk1_opm.i02";
connectAttr "solver.out[405]" "Rt_arm_fk1_opm.i10";
connectAttr "solver.out[406]" "Rt_arm_fk1_opm.i11";
connectAttr "solver.out[407]" "Rt_arm_fk1_opm.i12";
connectAttr "solver.out[408]" "Rt_arm_fk1_opm.i20";
connectAttr "solver.out[409]" "Rt_arm_fk1_opm.i21";
connectAttr "solver.out[410]" "Rt_arm_fk1_opm.i22";
connectAttr "solver.out[411]" "Rt_arm_fk1_opm.i30";
connectAttr "solver.out[412]" "Rt_arm_fk1_opm.i31";
connectAttr "solver.out[413]" "Rt_arm_fk1_opm.i32";
connectAttr "retarget.LeftMiddleFinger1" "LeftMiddleFinger1.im";
connectAttr "solver.out[630]" "Rt_finger_ring_1_opm.i00";
connectAttr "solver.out[631]" "Rt_finger_ring_1_opm.i01";
connectAttr "solver.out[632]" "Rt_finger_ring_1_opm.i02";
connectAttr "solver.out[633]" "Rt_finger_ring_1_opm.i10";
connectAttr "solver.out[634]" "Rt_finger_ring_1_opm.i11";
connectAttr "solver.out[635]" "Rt_finger_ring_1_opm.i12";
connectAttr "solver.out[636]" "Rt_finger_ring_1_opm.i20";
connectAttr "solver.out[637]" "Rt_finger_ring_1_opm.i21";
connectAttr "solver.out[638]" "Rt_finger_ring_1_opm.i22";
connectAttr "solver.out[639]" "Rt_finger_ring_1_opm.i30";
connectAttr "solver.out[640]" "Rt_finger_ring_1_opm.i31";
connectAttr "solver.out[641]" "Rt_finger_ring_1_opm.i32";
connectAttr "solver.out[546]" "Lf_finger_pinky_2_opm.i00";
connectAttr "solver.out[547]" "Lf_finger_pinky_2_opm.i01";
connectAttr "solver.out[548]" "Lf_finger_pinky_2_opm.i02";
connectAttr "solver.out[549]" "Lf_finger_pinky_2_opm.i10";
connectAttr "solver.out[550]" "Lf_finger_pinky_2_opm.i11";
connectAttr "solver.out[551]" "Lf_finger_pinky_2_opm.i12";
connectAttr "solver.out[552]" "Lf_finger_pinky_2_opm.i20";
connectAttr "solver.out[553]" "Lf_finger_pinky_2_opm.i21";
connectAttr "solver.out[554]" "Lf_finger_pinky_2_opm.i22";
connectAttr "solver.out[555]" "Lf_finger_pinky_2_opm.i30";
connectAttr "solver.out[556]" "Lf_finger_pinky_2_opm.i31";
connectAttr "solver.out[557]" "Lf_finger_pinky_2_opm.i32";
connectAttr "retarget.LeftThumb1" "LeftThumb1.im";
connectAttr "solver.out[342]" "Lf_arm_clav_opm.i00";
connectAttr "solver.out[343]" "Lf_arm_clav_opm.i01";
connectAttr "solver.out[344]" "Lf_arm_clav_opm.i02";
connectAttr "solver.out[345]" "Lf_arm_clav_opm.i10";
connectAttr "solver.out[346]" "Lf_arm_clav_opm.i11";
connectAttr "solver.out[347]" "Lf_arm_clav_opm.i12";
connectAttr "solver.out[348]" "Lf_arm_clav_opm.i20";
connectAttr "solver.out[349]" "Lf_arm_clav_opm.i21";
connectAttr "solver.out[350]" "Lf_arm_clav_opm.i22";
connectAttr "solver.out[351]" "Lf_arm_clav_opm.i30";
connectAttr "solver.out[352]" "Lf_arm_clav_opm.i31";
connectAttr "solver.out[353]" "Lf_arm_clav_opm.i32";
connectAttr "retarget.LeftIndexFinger" "LeftIndexFinger.im";
connectAttr "solver.out[534]" "Lf_finger_pinky_1_opm.i00";
connectAttr "solver.out[535]" "Lf_finger_pinky_1_opm.i01";
connectAttr "solver.out[536]" "Lf_finger_pinky_1_opm.i02";
connectAttr "solver.out[537]" "Lf_finger_pinky_1_opm.i10";
connectAttr "solver.out[538]" "Lf_finger_pinky_1_opm.i11";
connectAttr "solver.out[539]" "Lf_finger_pinky_1_opm.i12";
connectAttr "solver.out[540]" "Lf_finger_pinky_1_opm.i20";
connectAttr "solver.out[541]" "Lf_finger_pinky_1_opm.i21";
connectAttr "solver.out[542]" "Lf_finger_pinky_1_opm.i22";
connectAttr "solver.out[543]" "Lf_finger_pinky_1_opm.i30";
connectAttr "solver.out[544]" "Lf_finger_pinky_1_opm.i31";
connectAttr "solver.out[545]" "Lf_finger_pinky_1_opm.i32";
connectAttr "retarget.RightThumb_Z" "RightThumb_Z.im";
connectAttr "solver.out[327]" "Rt_leg_pv_opm.i30";
connectAttr "solver.out[328]" "Rt_leg_pv_opm.i31";
connectAttr "solver.out[329]" "Rt_leg_pv_opm.i32";
connectAttr "solver.out[390]" "Rt_arm_clav_opm.i00";
connectAttr "solver.out[391]" "Rt_arm_clav_opm.i01";
connectAttr "solver.out[392]" "Rt_arm_clav_opm.i02";
connectAttr "solver.out[393]" "Rt_arm_clav_opm.i10";
connectAttr "solver.out[394]" "Rt_arm_clav_opm.i11";
connectAttr "solver.out[395]" "Rt_arm_clav_opm.i12";
connectAttr "solver.out[396]" "Rt_arm_clav_opm.i20";
connectAttr "solver.out[397]" "Rt_arm_clav_opm.i21";
connectAttr "solver.out[398]" "Rt_arm_clav_opm.i22";
connectAttr "solver.out[399]" "Rt_arm_clav_opm.i30";
connectAttr "solver.out[400]" "Rt_arm_clav_opm.i31";
connectAttr "solver.out[401]" "Rt_arm_clav_opm.i32";
connectAttr "retarget.LeftThumb" "LeftThumb.im";
connectAttr "solver.out[303]" "Rt_leg_fk3_opm.i00";
connectAttr "solver.out[304]" "Rt_leg_fk3_opm.i01";
connectAttr "solver.out[305]" "Rt_leg_fk3_opm.i02";
connectAttr "solver.out[306]" "Rt_leg_fk3_opm.i10";
connectAttr "solver.out[307]" "Rt_leg_fk3_opm.i11";
connectAttr "solver.out[308]" "Rt_leg_fk3_opm.i12";
connectAttr "solver.out[309]" "Rt_leg_fk3_opm.i20";
connectAttr "solver.out[310]" "Rt_leg_fk3_opm.i21";
connectAttr "solver.out[311]" "Rt_leg_fk3_opm.i22";
connectAttr "solver.out[312]" "Rt_leg_fk3_opm.i30";
connectAttr "solver.out[313]" "Rt_leg_fk3_opm.i31";
connectAttr "solver.out[314]" "Rt_leg_fk3_opm.i32";
connectAttr "solver.out[330]" "head_opm.i00";
connectAttr "solver.out[331]" "head_opm.i01";
connectAttr "solver.out[332]" "head_opm.i02";
connectAttr "solver.out[333]" "head_opm.i10";
connectAttr "solver.out[334]" "head_opm.i11";
connectAttr "solver.out[335]" "head_opm.i12";
connectAttr "solver.out[336]" "head_opm.i20";
connectAttr "solver.out[337]" "head_opm.i21";
connectAttr "solver.out[338]" "head_opm.i22";
connectAttr "solver.out[339]" "head_opm.i30";
connectAttr "solver.out[340]" "head_opm.i31";
connectAttr "solver.out[341]" "head_opm.i32";
connectAttr "retarget.LeftMiddleFinger" "LeftMiddleFinger.im";
connectAttr "solver.out[252]" "Lf_leg_fk3_opm.i00";
connectAttr "solver.out[253]" "Lf_leg_fk3_opm.i01";
connectAttr "solver.out[254]" "Lf_leg_fk3_opm.i02";
connectAttr "solver.out[255]" "Lf_leg_fk3_opm.i10";
connectAttr "solver.out[256]" "Lf_leg_fk3_opm.i11";
connectAttr "solver.out[257]" "Lf_leg_fk3_opm.i12";
connectAttr "solver.out[258]" "Lf_leg_fk3_opm.i20";
connectAttr "solver.out[259]" "Lf_leg_fk3_opm.i21";
connectAttr "solver.out[260]" "Lf_leg_fk3_opm.i22";
connectAttr "solver.out[261]" "Lf_leg_fk3_opm.i30";
connectAttr "solver.out[262]" "Lf_leg_fk3_opm.i31";
connectAttr "solver.out[263]" "Lf_leg_fk3_opm.i32";
connectAttr "retarget.LeftPinkyFinger1" "LeftPinkyFinger1.im";
connectAttr "retarget.RightIndexFinger" "RightIndexFinger.im";
connectAttr "retarget.RightMiddleFinger" "RightMiddleFinger.im";
connectAttr "retarget.RightIndexFinger_Z" "RightIndexFinger_Z.im";
connectAttr "solver.out[426]" "Rt_arm_fk3_opm.i00";
connectAttr "solver.out[427]" "Rt_arm_fk3_opm.i01";
connectAttr "solver.out[428]" "Rt_arm_fk3_opm.i02";
connectAttr "solver.out[429]" "Rt_arm_fk3_opm.i10";
connectAttr "solver.out[430]" "Rt_arm_fk3_opm.i11";
connectAttr "solver.out[431]" "Rt_arm_fk3_opm.i12";
connectAttr "solver.out[432]" "Rt_arm_fk3_opm.i20";
connectAttr "solver.out[433]" "Rt_arm_fk3_opm.i21";
connectAttr "solver.out[434]" "Rt_arm_fk3_opm.i22";
connectAttr "solver.out[435]" "Rt_arm_fk3_opm.i30";
connectAttr "solver.out[436]" "Rt_arm_fk3_opm.i31";
connectAttr "solver.out[437]" "Rt_arm_fk3_opm.i32";
connectAttr "retarget.RightPinkyFinger" "RightPinkyFinger.im";
connectAttr "solver.out[642]" "Rt_finger_ring_2_opm.i00";
connectAttr "solver.out[643]" "Rt_finger_ring_2_opm.i01";
connectAttr "solver.out[644]" "Rt_finger_ring_2_opm.i02";
connectAttr "solver.out[645]" "Rt_finger_ring_2_opm.i10";
connectAttr "solver.out[646]" "Rt_finger_ring_2_opm.i11";
connectAttr "solver.out[647]" "Rt_finger_ring_2_opm.i12";
connectAttr "solver.out[648]" "Rt_finger_ring_2_opm.i20";
connectAttr "solver.out[649]" "Rt_finger_ring_2_opm.i21";
connectAttr "solver.out[650]" "Rt_finger_ring_2_opm.i22";
connectAttr "solver.out[651]" "Rt_finger_ring_2_opm.i30";
connectAttr "solver.out[652]" "Rt_finger_ring_2_opm.i31";
connectAttr "solver.out[653]" "Rt_finger_ring_2_opm.i32";
connectAttr "retarget.RightIndexFinger2" "RightIndexFinger2.im";
connectAttr "retarget.RightThumb1" "RightThumb1.im";
connectAttr "solver.out[666]" "Rt_finger_pinky_2_opm.i00";
connectAttr "solver.out[667]" "Rt_finger_pinky_2_opm.i01";
connectAttr "solver.out[668]" "Rt_finger_pinky_2_opm.i02";
connectAttr "solver.out[669]" "Rt_finger_pinky_2_opm.i10";
connectAttr "solver.out[670]" "Rt_finger_pinky_2_opm.i11";
connectAttr "solver.out[671]" "Rt_finger_pinky_2_opm.i12";
connectAttr "solver.out[672]" "Rt_finger_pinky_2_opm.i20";
connectAttr "solver.out[673]" "Rt_finger_pinky_2_opm.i21";
connectAttr "solver.out[674]" "Rt_finger_pinky_2_opm.i22";
connectAttr "solver.out[675]" "Rt_finger_pinky_2_opm.i30";
connectAttr "solver.out[676]" "Rt_finger_pinky_2_opm.i31";
connectAttr "solver.out[677]" "Rt_finger_pinky_2_opm.i32";
connectAttr "solver.out[240]" "Lf_leg_fk2_opm.i00";
connectAttr "solver.out[241]" "Lf_leg_fk2_opm.i01";
connectAttr "solver.out[242]" "Lf_leg_fk2_opm.i02";
connectAttr "solver.out[243]" "Lf_leg_fk2_opm.i10";
connectAttr "solver.out[244]" "Lf_leg_fk2_opm.i11";
connectAttr "solver.out[245]" "Lf_leg_fk2_opm.i12";
connectAttr "solver.out[246]" "Lf_leg_fk2_opm.i20";
connectAttr "solver.out[247]" "Lf_leg_fk2_opm.i21";
connectAttr "solver.out[248]" "Lf_leg_fk2_opm.i22";
connectAttr "solver.out[249]" "Lf_leg_fk2_opm.i30";
connectAttr "solver.out[250]" "Lf_leg_fk2_opm.i31";
connectAttr "solver.out[251]" "Lf_leg_fk2_opm.i32";
connectAttr "retarget.RightMiddleFinger1" "RightMiddleFinger1.im";
connectAttr "file2.oc" "wood.c";
connectAttr "bump2d1.o" "wood.n";
connectAttr "retarget.LeftIndexFinger2" "LeftIndexFinger2.im";
connectAttr "place2dTexture1.o" "file2.uv";
connectAttr "place2dTexture1.ofu" "file2.ofu";
connectAttr "place2dTexture1.ofv" "file2.ofv";
connectAttr "place2dTexture1.rf" "file2.rf";
connectAttr "place2dTexture1.reu" "file2.reu";
connectAttr "place2dTexture1.rev" "file2.rev";
connectAttr "place2dTexture1.vt1" "file2.vt1";
connectAttr "place2dTexture1.vt2" "file2.vt2";
connectAttr "place2dTexture1.vt3" "file2.vt3";
connectAttr "place2dTexture1.vc1" "file2.vc1";
connectAttr "place2dTexture1.ofs" "file2.fs";
connectAttr ":defaultColorMgtGlobals.cme" "file2.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "file2.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "file2.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "file2.ws";
connectAttr "solver.out[474]" "Lf_finger_index_2_opm.i00";
connectAttr "solver.out[475]" "Lf_finger_index_2_opm.i01";
connectAttr "solver.out[476]" "Lf_finger_index_2_opm.i02";
connectAttr "solver.out[477]" "Lf_finger_index_2_opm.i10";
connectAttr "solver.out[478]" "Lf_finger_index_2_opm.i11";
connectAttr "solver.out[479]" "Lf_finger_index_2_opm.i12";
connectAttr "solver.out[480]" "Lf_finger_index_2_opm.i20";
connectAttr "solver.out[481]" "Lf_finger_index_2_opm.i21";
connectAttr "solver.out[482]" "Lf_finger_index_2_opm.i22";
connectAttr "solver.out[483]" "Lf_finger_index_2_opm.i30";
connectAttr "solver.out[484]" "Lf_finger_index_2_opm.i31";
connectAttr "solver.out[485]" "Lf_finger_index_2_opm.i32";
connectAttr "solver.out[594]" "Rt_finger_index_2_opm.i00";
connectAttr "solver.out[595]" "Rt_finger_index_2_opm.i01";
connectAttr "solver.out[596]" "Rt_finger_index_2_opm.i02";
connectAttr "solver.out[597]" "Rt_finger_index_2_opm.i10";
connectAttr "solver.out[598]" "Rt_finger_index_2_opm.i11";
connectAttr "solver.out[599]" "Rt_finger_index_2_opm.i12";
connectAttr "solver.out[600]" "Rt_finger_index_2_opm.i20";
connectAttr "solver.out[601]" "Rt_finger_index_2_opm.i21";
connectAttr "solver.out[602]" "Rt_finger_index_2_opm.i22";
connectAttr "solver.out[603]" "Rt_finger_index_2_opm.i30";
connectAttr "solver.out[604]" "Rt_finger_index_2_opm.i31";
connectAttr "solver.out[605]" "Rt_finger_index_2_opm.i32";
connectAttr "retarget.LeftRingFinger1" "LeftRingFinger1.im";
connectAttr "retarget.LeftPinkyFinger_Z" "LeftPinkyFinger_Z.im";
connectAttr "solver.out[486]" "Lf_finger_mid_1_opm.i00";
connectAttr "solver.out[487]" "Lf_finger_mid_1_opm.i01";
connectAttr "solver.out[488]" "Lf_finger_mid_1_opm.i02";
connectAttr "solver.out[489]" "Lf_finger_mid_1_opm.i10";
connectAttr "solver.out[490]" "Lf_finger_mid_1_opm.i11";
connectAttr "solver.out[491]" "Lf_finger_mid_1_opm.i12";
connectAttr "solver.out[492]" "Lf_finger_mid_1_opm.i20";
connectAttr "solver.out[493]" "Lf_finger_mid_1_opm.i21";
connectAttr "solver.out[494]" "Lf_finger_mid_1_opm.i22";
connectAttr "solver.out[495]" "Lf_finger_mid_1_opm.i30";
connectAttr "solver.out[496]" "Lf_finger_mid_1_opm.i31";
connectAttr "solver.out[497]" "Lf_finger_mid_1_opm.i32";
connectAttr "retarget.LeftMiddleFinger_Z" "LeftMiddleFinger_Z.im";
connectAttr "solver.out[156]" "root_opm.i00";
connectAttr "solver.out[157]" "root_opm.i01";
connectAttr "solver.out[158]" "root_opm.i02";
connectAttr "solver.out[159]" "root_opm.i10";
connectAttr "solver.out[160]" "root_opm.i11";
connectAttr "solver.out[161]" "root_opm.i12";
connectAttr "solver.out[162]" "root_opm.i20";
connectAttr "solver.out[163]" "root_opm.i21";
connectAttr "solver.out[164]" "root_opm.i22";
connectAttr "solver.out[165]" "root_opm.i30";
connectAttr "solver.out[166]" "root_opm.i31";
connectAttr "solver.out[167]" "root_opm.i32";
connectAttr "file3.oa" "bump2d1.bv";
connectAttr "pCube1_geo_dup_geoSG.msg" "materialInfo1.sg";
connectAttr "wood.msg" "materialInfo1.m";
connectAttr "file2.msg" "materialInfo1.t" -na;
connectAttr "solver.out[558]" "Rt_finger_thumb_1_opm.i00";
connectAttr "solver.out[559]" "Rt_finger_thumb_1_opm.i01";
connectAttr "solver.out[560]" "Rt_finger_thumb_1_opm.i02";
connectAttr "solver.out[561]" "Rt_finger_thumb_1_opm.i10";
connectAttr "solver.out[562]" "Rt_finger_thumb_1_opm.i11";
connectAttr "solver.out[563]" "Rt_finger_thumb_1_opm.i12";
connectAttr "solver.out[564]" "Rt_finger_thumb_1_opm.i20";
connectAttr "solver.out[565]" "Rt_finger_thumb_1_opm.i21";
connectAttr "solver.out[566]" "Rt_finger_thumb_1_opm.i22";
connectAttr "solver.out[567]" "Rt_finger_thumb_1_opm.i30";
connectAttr "solver.out[568]" "Rt_finger_thumb_1_opm.i31";
connectAttr "solver.out[569]" "Rt_finger_thumb_1_opm.i32";
connectAttr "retarget.LeftMiddleFinger2" "LeftMiddleFinger2.im";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "pCube1_geo_dup_geoSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "pCube1_geo_dup_geoSG.message" ":defaultLightSet.message";
connectAttr "pCube1_geo_dup_geoSG.pa" ":renderPartition.st" -na;
connectAttr "wood.msg" ":defaultShaderList1.s" -na;
connectAttr "place2dTexture1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "bump2d1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "place2dTexture2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_leg_pv_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_leg_fk2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_leg_fk3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_leg_fk1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_leg_ik_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_mid_3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_mid_2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_mid_1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_pinky_3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_pinky_2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_pinky_1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_index_3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_index_2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_index_1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_thumb_3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_thumb_2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_thumb_1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_ring_3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_ring_2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_finger_ring_1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_mid_3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_mid_2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_mid_1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_pinky_3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_pinky_2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_pinky_1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_index_3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_index_2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_index_1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_thumb_3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_thumb_2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_thumb_1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_ring_3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_ring_2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_finger_ring_1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "spine_hips_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_arm_pv_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_arm_fk2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_arm_fk3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_arm_fk1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_arm_ik_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_arm_pv_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_arm_fk2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_arm_fk3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_arm_fk1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_arm_ik_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_leg_pv_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_leg_fk2_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_leg_fk3_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_leg_fk1_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_leg_ik_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "spine_chest_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Rt_arm_clav_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Lf_arm_clav_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "root_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "head_opm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "file2.msg" ":defaultTextureList1.tx" -na;
connectAttr "file3.msg" ":defaultTextureList1.tx" -na;
dataStructure -fmt "raw" -as "name=OffStruct:float=Offset";
dataStructure -fmt "raw" -as "name=externalContentTablZ:string=nodZ:string=key:string=upath:uint32=upathcrc:string=rpath:string=roles";
dataStructure -fmt "raw" -as "name=IdStruct:int32=ID";
dataStructure -fmt "raw" -as "name=OrgStruct:float[3]=Origin Point";
// End of scene.ma
