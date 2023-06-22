from typing import Dict, List, Tuple


async def batch_update_task_status(
    events: List[Tuple[str, Dict]]
) -> List[str]:
    ...
