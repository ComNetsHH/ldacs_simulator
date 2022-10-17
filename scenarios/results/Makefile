update-arq:
	cd ../../omnetpp-5.6.2/workspace/avionic-arq; git pull

update-rlc:
	cd ../../omnetpp-5.6.2/workspace/avionic-rlc; git pull

update-glue:
	cd ../../omnetpp-5.6.2/workspace/intairnet-linklayer-glue; git pull

update-wrapper:
	cd ../../omnetpp-5.6.2/workspace/intairnet-omnet-wrapper; git pull

update-radio:
	cd ../../omnetpp-5.6.2/workspace/intairnet-radio; git pull

update-mcsotdma:
	cd ../../omnetpp-5.6.2/workspace/mc-sotdma; git pull

update-intairnet-gpsr:
	cd ../../omnetpp-5.6.2/workspace/intairnet-gpsr; git pull
	
update-abstract-tdma:
	cd ../../omnetpp-5.6.2/workspace/tdma; git pull
	
update-traceBasedUdpApp:
	cd ../../omnetpp-5.6.2/workspace/intairnet-tracebasedapp; git pull

update-sim-model:
	git pull

# UPDATE pulls all changes from the currently selected branches of all repositories
update: update-arq update-rlc update-glue update-wrapper update-radio update-mcsotdma update-intairnet-gpsr update-abstract-tdma update-traceBasedUdpApp update-sim-model

NUM_CPUS = 1 # number of CPUs to allow OMNeT++ to use
SUFFIX = 

# BUILD-DEBUG compiles all libraries and then the simulation binary in DEBUG mode
build-debug:	
	cd ../../omnetpp-5.6.2/workspace/; \
	echo -e "\nARQ"; \
	cd avionic-arq/dev/cmake-build-debug; cmake -DCMAKE_BUILD_TYPE=Debug ..; make -j$(NUM_CPUS) tuhh_intairnet_arq; cd ../../..; \
	echo -e "\nRLC"; \
	cd avionic-rlc/cmake-build-debug; cmake -DCMAKE_BUILD_TYPE=Debug ..; make -j$(NUM_CPUS) tuhh_intairnet_rlc; cd ../..; \
	echo -e "\nGLUE"; \
	cd intairnet-linklayer-glue/cmake-build-debug; cmake -DCMAKE_BUILD_TYPE=Debug ..; make -j$(NUM_CPUS) intairnet_linklayer_glue; cd ../..; \
	echo -e "\nMCSOTDMA"; \
	cd mc-sotdma/cmake-build-debug; cmake -DCMAKE_BUILD_TYPE=Debug ..; make -j$(NUM_CPUS) tuhh_intairnet_mc-sotdma; cd ../..; \
	echo -e "\ntracebasedapp"; \
	cd intairnet-tracebasedapp/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET_dbg; make -j8 MODE=debug; cd ../..; \
	echo -e "\nRADIO"; \
	cd intairnet-radio/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET_dbg; make -j8 MODE=debug; cd ../..; \
	echo -e "\nGPSR"; \
	cd intairnet-gpsr/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET_dbg; make -j8 MODE=debug; cd ../..; \	
	echo -e "\nSIMULATION BINARY"; \
	cd intairnet-omnet-wrapper/intairnet-link-layer/src; opp_makemake -f --deep -O out -KINET4_PROJ=../../../inet4 -DINET_IMPORT -I../../../inet4 -I../../../intairnet-tracebasedapp/src -I../../../intairnet-radio/src -I../../../intairnet-gpsr/src -I../glue-lib-headers -I../avionic-rlc-headers -I../avionic-arq-headers -I../mc-sotdma-headers -I. -I../../../inet4/src -L../../../inet4/src -L../../../intairnet-tracebasedapp/out/gcc-debug/src/ -L../../../intairnet-radio/out/gcc-debug/src/ -L../../../intairnet-gpsr/out/gcc-debug/src/ -L../glue-lib -L../avionic-rlc -L../avionic-arq -L../mc-sotdma -lINET_dbg -lintairnet-tracebasedapp_dbg -lintairnet-radio_dbg -lintairnet-gpsr_dbg -lintairnet_linklayer_glue -ltuhh_intairnet_rlc -ltuhh_intairnet_arq -ltuhh_intairnet_mc-sotdma; make -j$(NUM_CPUS) MODE=debug; \
	echo -e "\nDon't forget to compile OMNeT++ itself and INET in debug mode, too! This target only compiles the LDACS libraries."

# BUILD-RELEASE compiles all libraries and then the simulation binary in RELEASE mode
build-release:
	cd ../../omnetpp-5.6.2/workspace/; \
	echo -e "\nARQ"; \
	cd avionic-arq/dev/cmake-build-release; cmake -DCMAKE_BUILD_TYPE=Release ..; make -j$(NUM_CPUS) tuhh_intairnet_arq; cd ../../..; \
	echo -e "\nRLC"; \
	cd avionic-rlc/cmake-build-release; cmake -DCMAKE_BUILD_TYPE=Release ..; make -j$(NUM_CPUS) tuhh_intairnet_rlc; cd ../..; \
	echo -e "\nGLUE"; \
	cd intairnet-linklayer-glue/cmake-build-release; cmake -DCMAKE_BUILD_TYPE=Release ..; make -j$(NUM_CPUS) intairnet_linklayer_glue; cd ../..; \
	echo -e "\nMCSOTDMA"; \
	cd mc-sotdma/cmake-build-release; cmake -DCMAKE_BUILD_TYPE=Release ..; make -j$(NUM_CPUS) tuhh_intairnet_mc-sotdma; cd ../..; \
	echo -e "\ntracebasedapp"; \
	cd intairnet-tracebasedapp/src; opp_makemake --make-so -f --deep -KINET_PROJ=../../inet4 -DINET_IMPORT -I../../inet4/src -L../../inet4/src -lINET; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nRADIO"; \
	cd intairnet-radio/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nGPSR"; \
	cd intairnet-gpsr/src; opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET; make -j$(NUM_CPUS) MODE=release; cd ../..; \
	echo -e "\nSIMULATION BINARY"; \
	cd intairnet-omnet-wrapper/intairnet-link-layer/src; opp_makemake -f --deep -O out -KINET4_PROJ=../../../inet4 -DINET_IMPORT -I../../../inet4 -I../../../intairnet-tracebasedapp/src -I../../../intairnet-radio/src -I../../../intairnet-gpsr/src -I../glue-lib-headers -I../avionic-rlc-headers -I../avionic-arq-headers -I../mc-sotdma-headers -I. -I../../../inet4/src -L../../../inet4/src -L../../../intairnet-tracebasedapp/out/gcc-release/src/ -L../../../intairnet-radio/out/gcc-release/src/ -L../../../intairnet-gpsr/out/gcc-release/src/ -L../glue-lib -L../avionic-rlc -L../avionic-arq -L../mc-sotdma -lINET -lintairnet-tracebasedapp -lintairnet-radio -lintairnet-gpsr -lintairnet_linklayer_glue -ltuhh_intairnet_rlc -ltuhh_intairnet_arq -ltuhh_intairnet_mc-sotdma; make -j$(NUM_CPUS) MODE=release

# GLOBAL VARIABLES  can be shared among all targets
# default binary in RELEASE mode
SIM_BINARY = ../../omnetpp-5.6.2/workspace/intairnet-omnet-wrapper/intairnet-link-layer/out/gcc-release/src/intairnet-link-layer
# debug binary
SIM_BINARY_DBG = ../../omnetpp-5.6.2/workspace/intairnet-omnet-wrapper/intairnet-link-layer/out/gcc-debug/src/intairnet-link-layer_dbg

# include .ned files
INCL = -n ../:./:../../omnetpp-5.6.2/workspace/inet4/src/:../../omnetpp-5.6.2/workspace/intairnet-omnet-wrapper/intairnet-link-layer/src/:../../omnetpp-5.6.2/workspace/intairnet-radio/src:../../omnetpp-5.6.2/workspace/intairnet-tracebasedapp/src:../../omnetpp-5.6.2/workspace/intairnet-gpsr/src

# QUICK SANITY CHECK SIMULATION
# This should quickly finish and tests the toolchain.
# After running, four graphs should've been created in the _imgs/ directory.
SANITY_CHECK_SEND_INT_START = 100	# First sending interval (ms)
SANITY_CHECK_SEND_INT_END = 200		# Last sending interval (ms)
SANITY_CHECK_SEND_INT_INCR = 50		# Increment sending intervals by this value (ms)
SANITY_CHECK_NUM_REPS = 2			# Number of repetitions
SANITY_CHECK_NUM_USERS = 5 6		# Number of users (one simulation with each)
sanity-check:	
	rm -rf SanityCheck/; \
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../sanity_check.ini -c SanityCheck $(INCL); \
	./convert-omnet-csv.sh simresults/SanityCheck; \
	python3 eval.py --dir simresults/SanityCheck --filename sanity_check --sending_interval_start $(SANITY_CHECK_SEND_INT_START) --sending_interval_stop $(SANITY_CHECK_SEND_INT_END) --sending_interval_step $(SANITY_CHECK_SEND_INT_INCR) --num_reps $(SANITY_CHECK_NUM_REPS) --n $(SANITY_CHECK_NUM_USERS) $(SUFFIX)

# RANDOM ACCESS
BC_MAC_RA_NUM_REPS = 10
BC_MAC_RA_NUM_USERS = 1 2 3 4 5 10 15 20 25 30
BC_MAC_RA_NUM_CANDIDATE_SLOTS = 5 10 20 30 40 60
BC_MAC_RA_TIME_SLOT_DURATION = 24 #ms
BC_MAC_RA_CONFIGNAME = RandomAccess
bc-mac-ra_sim:	
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../random_access.ini -c $(BC_MAC_RA_CONFIGNAME) $(INCL)

bc-mac-ra_parse:
	./convert-omnet-csv.sh simresults/$(BC_MAC_RA_CONFIGNAME)

bc-mac-ra_plot:
	python3 eval_random_access.py --dir simresults/$(BC_MAC_RA_CONFIGNAME) --filename bc_mac_ra --n $(BC_MAC_RA_NUM_USERS) --c $(BC_MAC_RA_NUM_CANDIDATE_SLOTS) --num_reps $(BC_MAC_RA_NUM_REPS) --time_slot_duration $(BC_MAC_RA_TIME_SLOT_DURATION) $(SUFFIX)

bc-mac-ra: bc-mac-ra_sim bc-mac-ra_parse bc-mac-ra_plot


BC_MAC_RA_SLOT_ADV_CONFIGNAME = RandomAccessSlotAdv
bc-mac-ra-slotadv_sim:
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../random_access.ini -c $(BC_MAC_RA_SLOT_ADV_CONFIGNAME) $(INCL)

bc-mac-ra-slotadv_parse:
	./convert-omnet-csv.sh simresults/$(BC_MAC_RA_SLOT_ADV_CONFIGNAME)

bc-mac-ra-slotadv_plot:
	python3 eval_random_access.py --dir simresults/$(BC_MAC_RA_SLOT_ADV_CONFIGNAME) --filename bc_mac_ra_slotadv --n $(BC_MAC_RA_NUM_USERS) --c $(BC_MAC_RA_NUM_CANDIDATE_SLOTS) --num_reps $(BC_MAC_RA_NUM_REPS) --time_slot_duration $(BC_MAC_RA_TIME_SLOT_DURATION) $(SUFFIX)

bc-mac-ra-slotadv: bc-mac-ra-slotadv_sim bc-mac-ra-slotadv_parse bc-mac-ra-slotadv_plot


# RANDOMIZED SLOTTED ALOHA
BC_MAC_ALOHA_NUM_REPS = 40
BC_MAC_ALOHA_NUM_USERS = 1 2 3 4 5 10 15 20 25 30
BC_MAC_ALOHA_CONFIGNAME_95 = RandomizedSlottedAloha95
BC_MAC_ALOHA_TARGET_RECEPTION_RATE_95 = 95
BC_MAC_ALOHA_TIME_SLOT_DURATION = 24 #ms
BC_MAC_ALOHA_DELAY_MAX_VAL = 8000
bc-mac-aloha-95_sim:	
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../random_access.ini -c $(BC_MAC_ALOHA_CONFIGNAME_95) $(INCL)

bc-mac-aloha-95_parse:
	./convert-omnet-csv.sh simresults/$(BC_MAC_ALOHA_CONFIGNAME_95)

bc-mac-aloha-95_plot:
	python3 eval_randomized_slotted_aloha.py --dir simresults/$(BC_MAC_ALOHA_CONFIGNAME_95) --filename bc_mac_aloha_95 --n $(BC_MAC_ALOHA_NUM_USERS) --num_reps $(BC_MAC_ALOHA_NUM_REPS) --target_reception_rate $(BC_MAC_ALOHA_TARGET_RECEPTION_RATE_95) --time_slot_duration $(BC_MAC_ALOHA_TIME_SLOT_DURATION) --delay_max_val $(BC_MAC_ALOHA_DELAY_MAX_VAL) $(SUFFIX)

bc-mac-aloha-95: bc-mac-aloha-95_sim bc-mac-aloha-95_parse bc-mac-aloha-95_plot

bc-mac-aloha-95_clean:
	rm simresults/$(BC_MAC_ALOHA_CONFIGNAME_95)/*

BC_MAC_ALOHA_CONFIGNAME_75 = RandomizedSlottedAloha75
BC_MAC_ALOHA_TARGET_RECEPTION_RATE_75 = 75
bc-mac-aloha-75_sim:	
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../random_access.ini -c $(BC_MAC_ALOHA_CONFIGNAME_75) $(INCL)

bc-mac-aloha-75_parse:
	./convert-omnet-csv.sh simresults/$(BC_MAC_ALOHA_CONFIGNAME_75)

bc-mac-aloha-75_plot:
	python3 eval_randomized_slotted_aloha.py --dir simresults/$(BC_MAC_ALOHA_CONFIGNAME_75) --filename bc_mac_aloha_75 --n $(BC_MAC_ALOHA_NUM_USERS) --num_reps $(BC_MAC_ALOHA_NUM_REPS) --target_reception_rate $(BC_MAC_ALOHA_TARGET_RECEPTION_RATE_75) --time_slot_duration $(BC_MAC_ALOHA_TIME_SLOT_DURATION) --delay_max_val $(BC_MAC_ALOHA_DELAY_MAX_VAL) $(SUFFIX)

bc-mac-aloha-75: bc-mac-aloha-75_sim bc-mac-aloha-75_parse bc-mac-aloha-75_plot

bc-mac-aloha-75_clean:
	rm simresults/$(BC_MAC_ALOHA_CONFIGNAME_75)/*

BC_MAC_ALOHA_CONFIGNAME_50 = RandomizedSlottedAloha50
BC_MAC_ALOHA_TARGET_RECEPTION_RATE_50 = 50
bc-mac-aloha-50_sim:	
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../random_access.ini -c $(BC_MAC_ALOHA_CONFIGNAME_50) $(INCL)

bc-mac-aloha-50_parse:
	./convert-omnet-csv.sh simresults/$(BC_MAC_ALOHA_CONFIGNAME_50); \
	./convert-vec-omnet-csv.sh simresults/$(BC_MAC_ALOHA_CONFIGNAME_50)

bc-mac-aloha-50_plot:
	python3 eval_randomized_slotted_aloha.py --dir simresults/$(BC_MAC_ALOHA_CONFIGNAME_50) --filename bc_mac_aloha_50 --n $(BC_MAC_ALOHA_NUM_USERS) --num_reps $(BC_MAC_ALOHA_NUM_REPS) --target_reception_rate $(BC_MAC_ALOHA_TARGET_RECEPTION_RATE_50) --time_slot_duration $(BC_MAC_ALOHA_TIME_SLOT_DURATION) --delay_max_val $(BC_MAC_ALOHA_DELAY_MAX_VAL) $(SUFFIX); \
	python3 eval_randomized_slotted_aloha_delays.py --dir simresults/$(BC_MAC_ALOHA_CONFIGNAME_50) --filename bc_mac_aloha_50_delays --n $(BC_MAC_ALOHA_NUM_USERS) --num_reps $(BC_MAC_ALOHA_NUM_REPS) --time_slot_duration $(BC_MAC_ALOHA_TIME_SLOT_DURATION) $(SUFFIX)

bc-mac-aloha-50: bc-mac-aloha-50_sim bc-mac-aloha-50_parse bc-mac-aloha-50_plot

bc-mac-aloha-50_clean:
	rm simresults/$(BC_MAC_ALOHA_CONFIGNAME_50)/*


BC_MAC_ALOHA_CONFIGNAME_OPT = RandomizedSlottedAlohaOptimal
BC_MAC_ALOHA_TARGET_RECEPTION_RATE_OPT = 37
bc-mac-aloha-opt_sim:
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../random_access.ini -c $(BC_MAC_ALOHA_CONFIGNAME_OPT) $(INCL)

bc-mac-aloha-opt_parse:
	./convert-omnet-csv.sh simresults/$(BC_MAC_ALOHA_CONFIGNAME_OPT); \
	./convert-vec-omnet-csv.sh simresults/$(BC_MAC_ALOHA_CONFIGNAME_OPT)

bc-mac-aloha-opt_plot:
	python3 eval_randomized_slotted_aloha.py --dir simresults/$(BC_MAC_ALOHA_CONFIGNAME_OPT) --filename bc_mac_aloha_opt --n $(BC_MAC_ALOHA_NUM_USERS) --num_reps $(BC_MAC_ALOHA_NUM_REPS) --target_reception_rate $(BC_MAC_ALOHA_TARGET_RECEPTION_RATE_OPT) --time_slot_duration $(BC_MAC_ALOHA_TIME_SLOT_DURATION) --delay_max_val $(BC_MAC_ALOHA_DELAY_MAX_VAL) $(SUFFIX); \
	python3 eval_randomized_slotted_aloha_delays.py --dir simresults/$(BC_MAC_ALOHA_CONFIGNAME_OPT) --filename bc_mac_aloha_opt_delays --n $(BC_MAC_ALOHA_NUM_USERS) --num_reps $(BC_MAC_ALOHA_NUM_REPS) --time_slot_duration $(BC_MAC_ALOHA_TIME_SLOT_DURATION) $(SUFFIX)

bc-mac-aloha-opt: bc-mac-aloha-opt_sim bc-mac-aloha-opt_parse bc-mac-aloha-opt_plot

bc-mac-aloha-opt_clean:
	rm simresults/$(BC_MAC_ALOHA_CONFIGNAME_OPT)/*

BC_MAC_ALOHA_CONFIGNAME_25 = RandomizedSlottedAloha25
BC_MAC_ALOHA_TARGET_RECEPTION_RATE_25 = 25
bc-mac-aloha-25_sim:	
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../random_access.ini -c $(BC_MAC_ALOHA_CONFIGNAME_25) $(INCL)

bc-mac-aloha-25_parse:
	./convert-omnet-csv.sh simresults/$(BC_MAC_ALOHA_CONFIGNAME_25)

bc-mac-aloha-25_plot:
	python3 eval_randomized_slotted_aloha.py --dir simresults/$(BC_MAC_ALOHA_CONFIGNAME_25) --filename bc_mac_aloha_25 --n $(BC_MAC_ALOHA_NUM_USERS) --num_reps $(BC_MAC_ALOHA_NUM_REPS) --target_reception_rate $(BC_MAC_ALOHA_TARGET_RECEPTION_RATE_25) --time_slot_duration $(BC_MAC_ALOHA_TIME_SLOT_DURATION) --delay_max_val $(BC_MAC_ALOHA_DELAY_MAX_VAL) $(SUFFIX)

bc-mac-aloha-25: bc-mac-aloha-25_sim bc-mac-aloha-25_parse bc-mac-aloha-25_plot

bc-mac-aloha-all_plot:
	python3 eval_randomized_slotted_aloha_aggregate.py --dirs simresults/$(BC_MAC_ALOHA_CONFIGNAME_95) simresults/$(BC_MAC_ALOHA_CONFIGNAME_75) simresults/$(BC_MAC_ALOHA_CONFIGNAME_50) simresults/$(BC_MAC_ALOHA_CONFIGNAME_OPT) --filename bc_mac_aloha_all --n $(BC_MAC_ALOHA_NUM_USERS) --num_reps $(BC_MAC_ALOHA_NUM_REPS) --target_reception_rates $(BC_MAC_ALOHA_TARGET_RECEPTION_RATE_95) $(BC_MAC_ALOHA_TARGET_RECEPTION_RATE_75) $(BC_MAC_ALOHA_TARGET_RECEPTION_RATE_50) $(BC_MAC_ALOHA_TARGET_RECEPTION_RATE_OPT) --time_slot_duration $(BC_MAC_ALOHA_TIME_SLOT_DURATION) $(SUFFIX)

bc-mac-aloha-all_clean: bc-mac-aloha-95_clean bc-mac-aloha-75_clean bc-mac-aloha-50_clean bc-mac-aloha-opt_clean	

# OPTIMAL COLLISION PROBABILITY
bc-mac-opt: 
	python optimize_target_collsion_rate.py 

# LINK ESTABLISHMENT TIMES
PP_LINK_ESTBL_TEST_CONFIGNAME = PPLinkEstablishmentTimes
PP_LINK_ESTBL_TEST_NUM_REPS = 10
PP_LINK_ESTBL_TEST_NUM_PAIRS = 1
PP_LINK_ESTBL_TEST_NUM_BROADCAST_USERS = 0 5 10 15 20 25 30
pp-link-estbl-test_sim:
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../link_establishment.ini -c $(PP_LINK_ESTBL_TEST_CONFIGNAME) $(INCL)

pp-link-estbl-test_parse:
	./convert-omnet-csv.sh simresults/$(PP_LINK_ESTBL_TEST_CONFIGNAME); \
	./convert-vec-omnet-csv.sh simresults/$(PP_LINK_ESTBL_TEST_CONFIGNAME)

pp-link-estbl-test_plot:
	python3 eval_link_estbl_time.py --dir simresults/$(PP_LINK_ESTBL_TEST_CONFIGNAME) --filename link_estbl_time --num_reps $(PP_LINK_ESTBL_TEST_NUM_REPS) --n $(PP_LINK_ESTBL_TEST_NUM_PAIRS) --m $(PP_LINK_ESTBL_TEST_NUM_BROADCAST_USERS) $(SUFFIX)

pp-link-estbl-test: pp-link-estbl-test_sim pp-link-estbl-test_parse pp-link-estbl-test_plot

pp-link-estbl-test_clean:
	rm simresults/$(PP_LINK_ESTBL_TEST_CONFIGNAME)/*

# PP VOICE
PP_VOICE_NAIVE_CONFIGNAME = PPVoice
PP_VOICE_TIME_SLOT_DURATION = 24
pp-voice_sim:
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../link_establishment.ini -c $(PP_VOICE_NAIVE_CONFIGNAME) $(INCL)

pp-voice_parse:
	./convert-omnet-csv.sh simresults/$(PP_VOICE_NAIVE_CONFIGNAME); \
	./convert-vec-omnet-csv.sh simresults/$(PP_VOICE_NAIVE_CONFIGNAME)

pp-voice_plot:
	python3 eval_pp_voice.py --dir simresults/$(PP_VOICE_NAIVE_CONFIGNAME) --filename pp_voice_n_10 --time_slot_duration $(PP_VOICE_TIME_SLOT_DURATION) $(SUFFIX)

pp-voice: pp-voice_sim pp-voice_parse pp-voice_plot

pp-voice_clean:
	rm simresults/$(PP_VOICE_NAIVE_CONFIGNAME)/*


# BROADCAST VOICE
BROADCAST_VOICE_CONFIGNAME = BroadcastVoice
BROADCAST_VOICE_NUM_REPS = 10
BROADCAST_VOICE_NUM_USERS = 1 5 10 15 20 25 30
BROADCAST_VOICE_CHANNEL_ERROR = 0 0.05 0.10 0.15
BROADCAST_VOICE_TIME_SLOT_DURATION = 24
broadcast-voice_sim:
	opp_runall -j$(NUM_CPUS) $(SIM_BINARY) ../random_access.ini -c $(BROADCAST_VOICE_CONFIGNAME) $(INCL)

broadcast-voice_parse:
	./convert-omnet-csv.sh simresults/$(BROADCAST_VOICE_CONFIGNAME)

broadcast-voice_plot:
	python3 eval_broadcast_voice.py --dir simresults/$(BROADCAST_VOICE_CONFIGNAME) --filename broadcast_voice --num_users $(BROADCAST_VOICE_NUM_USERS) --channel_errors $(BROADCAST_VOICE_CHANNEL_ERROR) --num_reps $(BROADCAST_VOICE_NUM_REPS) --target 0.367 $(SUFFIX)

broadcast-voice: broadcast-voice_sim broadcast-voice_parse broadcast-voice_plot

broadcast-voice_clean:
	rm simresults/$(BROADCAST_VOICE_CONFIGNAME)/*