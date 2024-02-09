import { Card } from 'react-bootstrap';
import '../styles/RecipeInList.css';


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
        </Card>
}