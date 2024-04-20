import { Card, Col, Container, Image, Row } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Recipe } from '../types/interfaces';
import { RecipeDirectionsCard } from '../components/RecipeDirectionsCard';
import { RecipeIngredientList } from '../components/RecipeIngredientList';
import { RecipeInfoCard } from '../components/RecipeInfoCard';
import styles from '../styles/RecipeDetail.module.css';
import { downloadImage, getRecipeDetail } from '../api/recipesApi';


interface Params {
    id: string;
    [key: string]: string;
}

export function RecipeDetail() {
    const [recipe, setRecipe] = useState<Recipe>();
    const [imageSrc, setImageSrc] = useState<string>('');
    const { id = '' } = useParams<Params>();

    useEffect(() => {
        const fetchRecipe = async () => {
            getRecipeDetail(id).then(res => {
                if (res.status === 200) {
                    setRecipe(res.data);
                } else {
                    console.log('Failed to fetch recipe');
                }
            });
        };
        const fetchImage = async () => {
            downloadImage(String(id)).then(res => {
                if (res.status === 200) {
                        const url: string = URL.createObjectURL(res.data);
                        setImageSrc(url);
                } else {
                    console.log('Failed to fetch image');
                }
            });
        };
        fetchImage();
        fetchRecipe();
    }, [id]);

    return (
        recipe ? (
            <Container className="pb-4">
                <Row md={2} xs={1} className="d-flex align-items-center g-2 mt-2">
                    <Col className={`${styles.image_container}`}>
                        <Image
                            src={imageSrc}
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
        ) : null
    )   
}
