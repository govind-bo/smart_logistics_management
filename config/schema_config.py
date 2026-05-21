PK_MAP = {
    'shipments' : 'shipment_id',
    'shipment_tracking': 'tracking_id',
    'courier_staff': 'courier_id',
    'routes': 'route_id',
    'warehouses': 'warehouse_id',
    'costs': 'shipment_id'
}

# FK_MAP element represent (child_table, child_fk, parent_table, parent_pk )
FK_MAP = [
    ('shipments', 'courier_id', 'courier_staff', 'courier_id'),
    ('shipment_tracking', 'shipment_id', 'shipments', 'shipment_id'),
    ('costs', 'shipment_id', 'shipments', 'shipment_id')
]