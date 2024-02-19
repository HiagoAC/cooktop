import { Button, Card } from 'react-bootstrap';
import { BadgeStack } from './BadgeStack';
import '../styles/RecipeInfoCard.css';
import editIcon from '../assets/edit_icon.svg';


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
            <Card.Subtitle className="mb-2 text-muted d-flex align-items-center">
                <Button className="edit-button">
                    <img
                        src={editIcon}
                        alt="prep time"
                        className="edit-icon"
                    />
                </Button>
                <span>
                    {recipe_type} &middot; {time_minutes} minutes
                </span>
            </Card.Subtitle>
            <Card.Body>
                <span>{description}</span>
                <BadgeStack items={tags} />
            </Card.Body>
        </Card>
    )
}
