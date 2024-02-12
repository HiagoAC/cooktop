import { Badge, Stack } from 'react-bootstrap';
import '../styles/TagBadgeStack.css';


type TagBadgeStackProps = {
    tags: Array<string>
}


export function TagBadgeStack({tags}: TagBadgeStackProps) {
    return (
        <Stack direction="horizontal" gap={1} className="mt-2">
            {tags.map(tag => (
                <Badge bg="custom" className="custom-badge">{tag}</Badge>
            ))}
        </Stack>
    )
}
