import { v4 as uuidv4 } from 'uuid';
import { Stack } from 'react-bootstrap';
import { Badge } from './Badge'


type BadgeStackProps = {
    items?: Array<string>
}


export function BadgeStack({items = [] }: BadgeStackProps) {
    return (
        <Stack direction="horizontal" gap={1} className="mt-2">
            {items.map(item => (
                <Badge key={uuidv4()} item={item} />
            ))}
        </Stack>
    )
}
