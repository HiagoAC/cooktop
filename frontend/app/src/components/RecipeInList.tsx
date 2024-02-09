import { Badge, Card, Stack } from 'react-bootstrap';
import '../styles/RecipeInList.css';
import clockIcon from '../assets/clock_icon.svg';


type RecipeInListProps = {
    id: number,
    title: string,
    time_minutes: number,
    tags: Array<string>,
    image: string
}


export function RecipeInList({ id, title, time_minutes, tags, image }:
    RecipeInListProps) {
        return <Card>
            <Card.Img
                variant="top"
                src={image}
                height="200px"
                className="card-img"
            />
            <Card.Body className="d-flex flex-column">
                <Card.Title>{title}</Card.Title>
                <Card.Text>
                    <span>
                        <div className="icon-container">
                            <img
                                src={clockIcon}
                                alt="pre time"
                                className="clock-icon"
                            />
                        </div> {time_minutes} min
                    </span>
                    <Stack direction="horizontal" gap={1} className="mt-2">
                        {tags.map(tag => (
                        <Badge bg="custom" className="custom-badge">{tag}</Badge>
                        ))}
                    </Stack>
                </Card.Text>
            </Card.Body>
        </Card>
}