
def export_template(path_to_aster_root,path_to_comm_file,path_to_mess_file):
    temp_text = f"""
        P actions make_etude
        P aster_root {path_to_aster_root}
        P consbtc oui
        P corefilesize unlimited
        P cpresok RESNOOK
        P debug nodebug
        P facmtps 1
        P follow_output yes
        P lang en
        P memjob 5120000
        P memory_limit 5000.0
        P mode interactif
        P mpi_nbcpu 1
        P mpi_nbnoeud 1
        P rep_trav /tmp/dell7490-dell7490-interactif_11958
        P testlist verification sequential
        P time_limit 72000.0
        P tpsjob 1201
        P version stable
        A memjeveux 625.0
        A tpmax 72000.0
        F comm {path_to_comm_file} D  1
        F mess {path_to_mess_file} R  6
        """
    return temp_text