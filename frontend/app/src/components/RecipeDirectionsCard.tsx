import { v4 as uuidv4 } from 'uuid';
import { Card, Stack } from 'react-bootstrap';


type Props = {
    directions: Array<string>,
}


export function RecipeDirectionsCard({directions}: Props) {

    return (
        <Card className="p-3 mt-2">
            <Card.Title>Directions</Card.Title>
            <Card.Body>
                <Stack direction="vertical" gap={1} className="mt-2">
                    {directions.map((direction: string, index: number) => (
                        <div key={uuidv4()} className="mb-3">
                            <h6>Step {index + 1}</h6>
                            {direction}
                        </div>
                    ))}
                </Stack>
            </Card.Body>
        </Card>
    )
}
