from datetime import datetime
from fastapi import APIRouter

from ..database import Flow
from ..serializers.flows import FlowSerializer

router = APIRouter()


@router.get('')
async def get_flows(source: str = None, start: str = None, end: str = None):
    # Sanitize start and end
    start = start[:-1] if start[-1] == 'Z' else start
    end = end[:-1] if end[-1] == 'Z' else end

    query = {}
    if source:
        query['source'] = {'$eq': source}
    if start:
        query['timestamp'] = {'$gte': datetime.fromisoformat(start)}
    if end:
        query['timestamp'] = {'$lte': datetime.fromisoformat(end)}
        
    # Return first occurrence of each location
    locations = set()
    ret = []
    for flow in Flow.find(query):
        if flow['location'] not in locations:
            locations.add(flow['location'])
            ret.append(FlowSerializer(**flow))
    return ret
