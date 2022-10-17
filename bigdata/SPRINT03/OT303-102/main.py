from include import logger
import subprocess
import os

"""
if [ -f $hadoopstrjar ]; then echo $hadoopstrjar: OK; else echo $hadoopstrjar: NOT FOUND; fi
if hdfs dfs -test -f $small_xml; then echo $small_xml: OK; else echo $small_xml: NOT FOUND; fi
if hdfs dfs -test -f $big_xml; then echo $big_xml: OK; else echo $big_xml: NOT FOUND; fi
if [ -f $mapper ]; then echo $mapper: OK; else echo $mapper: NOT FOUND; fi
if [ -f $reducer ]; then echo $reducer: OK; else echo $reducer: NOT FOUND; fi
"""
log = logger.set_logger(logger_name=f"{logger.get_rel_path(__file__)}")


def run_bash(in_file_cmd):
    cmd_stdout = subprocess.run(in_file_cmd, shell=True, stdout=subprocess.PIPE)
    cmd_stdout = cmd_stdout.stdout.decode().strip()
    return cmd_stdout


@logger.log_basics(log)
def main():
    find_hadoopstrjar_cmd = 'find ~ | grep --p ".*/lib/.*hadoop.*streaming.*.jar"'
    find_hadoopstrjar_cmd_out = subprocess.run(
        find_hadoopstrjar_cmd, capture_output=True, shell=True
    )

    # Initialize all the file variables
    hadoopstrjar = find_hadoopstrjar_cmd_out.stdout.decode().strip()

    hdfs_xml_path = os.path.join(os.sep, "alkemybigdata", "Stack_Overflow_11-2010")
    hdfs_xml_path_out = os.path.join(hdfs_xml_path, "output")
    hdfs_xml_file_out = os.path.join(hdfs_xml_path_out, "part-00000")

    hdfs_small_xml = os.path.join(
        hdfs_xml_path, "112010_Meta_Stack_Overflow", "posts.xml"
    )

    hdfs_big_xml = os.path.join(hdfs_xml_path, "112010_Stack_Overflow", "posts.xml")

    mapper = {}
    reducer = {}

    for i in [1, 2, 3]:
        mapper[i] = os.path.join(os.getcwd(), "include", f"mapper{i}.py")
        reducer[i] = os.path.join(os.getcwd(), "include", f"reducer{i}.py")

    # Check file existence

    os_files = [hadoopstrjar, *list(mapper.values()), *list(reducer.values())]
    hdfs_xmls = [hdfs_small_xml, hdfs_big_xml]

    # we validate this through bash as I am keeping the same already done logic,
    # it could be done with python but I prefer to keep consistency with the previous steps
    os_files_cmd = [
        f"if [ -f {os_file} ]; then echo {os_file}: OK; else echo {os_file}: NOT FOUND; fi"
        for os_file in os_files
    ]
    hdfs_xmls_cmd = [
        f"if hdfs dfs -test -f {hdfs_file}; then echo {hdfs_file}: OK; else echo {hdfs_file}: NOT FOUND; fi"
        for hdfs_file in hdfs_xmls
    ]

    chk_cmd_stdout = []

    for file_cmd in [*os_files_cmd, *hdfs_xmls_cmd]:
        cmd_stdout = run_bash(file_cmd)
        log.info(cmd_stdout)
        chk_cmd_stdout.append(cmd_stdout)

    for chk in chk_cmd_stdout:
        if chk.endswith("NOT FOUND"):
            raise FileNotFoundError

    # Run Hadoop for requirements 1,2 and 3, for both big and small posts.xml

    for i in [1, 2, 3]:
        for hdfs_xml in hdfs_xmls:
            hadoop_cmd = f'hadoop jar {hadoopstrjar} -input {hdfs_xml} -output {hdfs_xml_path_out} -mapper "python3 {mapper[i]}" -reducer "python3 {reducer[i]}"'
            log.info(f'Processing:\n{hadoop_cmd}')

            # Delete output directory if ixists (Hadoop fails otherwise)
            run_bash(f"hdfs dfs -rm -R -skipTrash {hdfs_xml_path_out}")
            run_bash(hadoop_cmd)

            # Log the results up to 15 lines
            cmd_stdout = run_bash(f"hdfs dfs -cat {hdfs_xml_file_out} | head -15")
            log.info(f'Output:\n{cmd_stdout}')


if __name__ == "__main__":
    main()
