from pathlib import Path
from api_mp_vm.client import MaxPatrolVMClient
from api_mp_vm.pipeline_service import MPVMPipelineService
from api_mp_vm.mp_vm_variables import mpvm_base_url, MPVM_HTTPS_VERIFY
import logging
logger = logging.getLogger(__name__)
def main_api_mp_vm() -> bool:
    """Глобальный ETL-конвейер обработки уязвимостей MaxPatrol VM."""
    logger.info("Initializing modern main_api_mp_vm pipeline.")
    client = MaxPatrolVMClient(base_url=mpvm_base_url, verify_ssl=MPVM_HTTPS_VERIFY)
    pipeline = MPVMPipelineService()
    if not client.authenticate():
        logger.critical("Pipeline aborted: MaxPatrol VM Authentication Failed.")
        return False
    base_project_dir = Path(__file__).resolve().parent.parent
    integration_folder = base_project_dir / "intergrations"
    if not integration_folder.exists():
        logger.error(f"Target integrations directory data source mapping not found: {integration_folder}")
        return False
    success_count = 0
    for subdir in integration_folder.iterdir():
        if not subdir.is_dir() or subdir.name == "jira-check":
            logger.debug(f"Skipping integration path directory context: {subdir.name}")
            continue
        pdql_files = list(subdir.glob("*.pdql"))
        for pdql_file in pdql_files:
            query_name = pdql_file.stem
            logger.info(f"Processing query compilation hook: {query_name}")
            try:
                pdql_query = pdql_file.read_text(encoding="utf-8").replace("\n", " ").replace("\r", " ")
            except Exception as e:
                logger.error(f"IO Error reading query payload file {pdql_file}: {e}")
                continue
            pdql_token = client.get_pdql_token(pdql_query)
            if not pdql_token:
                continue
            csv_data = client.fetch_grid_data(pdql_token)
            if not csv_data:
                logger.error(f"Data stream collection is empty for query: {query_name}")
                continue
            import csv
            from io import StringIO
            raw_records_list = []
            with StringIO(csv_data) as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    clean_row = {k.strip('"'): v.strip('"') for k, v in row.items() if k}
                    raw_records_list.append(clean_row)
            enriched_data = pipeline.enrich_and_clean(raw_records_list)
            if pipeline.save_output_files(enriched_data, subdir.name, query_name):
                success_count += 1
    if success_count > 0:
        logger.info(f"Pipeline orchestration flow finalized. Successfully processed {success_count} jobs.")
        return True
    logger.error("Pipeline finished execution sequence, but 0 data structures updated.")
    return False
