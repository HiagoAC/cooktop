import { Card, Col, Container, Image, Row } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import { recipesDetail, Recipe } from '../data/recipe_detail';
import { RecipeDirectionsCard } from '../components/RecipeDirectionsCard';
import { RecipeIngredientList } from '../components/RecipeIngredientList';
import { RecipeInfoCard } from '../components/RecipeInfoCard';
import styles from '../styles/RecipeDetail.module.css';


interface Params {
    id?: string;
}

export function RecipeDetail() {
    const { id } = useParams<Params>();
    if (!id || !Object.prototype.hasOwnProperty.call(recipesDetail, id)) {
        return <div>Recipe not found</div>
    };
    const recipe: Recipe = recipesDetail[id];

    return (
        <Container className="pb-4">
            <Row md={2} xs={1} className="d-flex align-items-center g-2 mt-2">
                <Col className={`${styles.image_container}`}>
                    <Image
                        src={recipe.image}
                        alt={recipe.title}
                        className={`${styles.image}`}
                        rounded
                    />
                </Col>
                <Col>
                    <RecipeInfoCard id={id} recipe={recipe}/>
                </Col>
            </Row>
            <Row md={2} xs={1} className="align-top g-2 mt-2">
                <Col md={4}>
                    <RecipeIngredientList ingredients={recipe.ingredients}/>
                    <Card className="p-3 mt-2">
                        <Card.Title>Notes</Card.Title>
                        <Card.Body>{recipe.notes}</Card.Body>
                    </Card>
                </Col>
                <Col md={8}>
                    <RecipeDirectionsCard directions={recipe.directions}/>
                </Col>
            </Row>
        </Container>
    )   
}
