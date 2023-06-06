import get_stats
import merge_cpts
import merge_workloads
from newFolder import write_xls

if __name__ == '__main__':
    get_stats.get_stats()
    merge_cpts.merge_cpts()
    merge_workloads.merge_workloads()
    write_xls.write_xls()