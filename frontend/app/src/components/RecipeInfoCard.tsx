import { Button, Card } from 'react-bootstrap';
import { BadgeStack } from './BadgeStack';
import { Recipe, recipeTypeLabels } from '../data/recipe_detail';
import styles from '../styles/RecipeInfoCard.module.css';
import editIcon from '../assets/edit_icon.svg';
import { Link } from 'react-router-dom';

interface Props {
    id: string,
    recipe: Recipe
}

export function RecipeInfoCard({id, recipe}: Props) {

    return (
        <Card className={`p-3 ${styles.info_card}`}>
            <Card.Title className={`${styles.info_card_title}`}>
                {recipe.title}
            </Card.Title>
            <Card.Subtitle
                className="mb-2 text-muted d-flex align-items-center"
            >
                <Button className={`${styles.edit_button}`}>
                    <img
                        src={editIcon}
                        alt="edit"
                        className={`${styles.edit_icon}`}
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
