import { Card } from 'react-bootstrap';
import { BadgeStack } from './BadgeStack';
import '../styles/RecipeInfoCard.css';


interface Props {
    title: string,
    recipe_type: string,
    time_minutes: number,
    description: string,
    tags: string[],
}


export function RecipeInfoCard(
    {title, recipe_type, time_minutes, description, tags}
    : Props) {

    return (
        <Card className="info-card p-3">
            <Card.Title className="info-card-title">
                {title}
            </Card.Title>
            <Card.Subtitle className="mb-2 text-muted">
                {recipe_type} &middot; {time_minutes} minutes
            </Card.Subtitle>
            <Card.Body>
                <span>{description}</span>
                <BadgeStack items={tags} />
            </Card.Body>
        </Card>
    )
}
