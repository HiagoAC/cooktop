import { Button, Card } from 'react-bootstrap';
import { BadgeStack } from './BadgeStack';
import { Recipe, recipeTypeLabels } from '../data/recipe_detail';
import '../styles/RecipeInfoCard.css';
import editIcon from '../assets/edit_icon.svg';
import { Link } from 'react-router-dom';

interface Props {
    id: string,
    recipe: Recipe
}

export function RecipeInfoCard({id, recipe}: Props) {

    return (
        <Card className="info-card p-3">
            <Card.Title className="info-card-title">
                {recipe.title}
            </Card.Title>
            <Card.Subtitle
                className="mb-2 text-muted d-flex align-items-center"
            >
                <Button className="edit-button">
                    <img
                        src={editIcon}
                        alt="prep time"
                        className="edit-icon"
                    />
                    <Link
                        to={`/recipes/${id}/edit`}
                        state={{ recipe: recipe }}
                        className="stretched-link"
                    />
                </Button>
                <span>
                    {recipeTypeLabels[recipe.recipe_type]} &middot; {recipe.time_minutes} minutes
                </span>
            </Card.Subtitle>
            <Card.Body>
                <span>{recipe.description}</span>
                <BadgeStack items={recipe.tags} />
            </Card.Body>
        </Card>
    )
}